"""Isolated, read-only configuration checks; never builds, downloads or runs code.

Implements only the JSON Schema keyword subset used by the sibling v1 schemas.
Semantic checks are additional to the machine-readable schema contracts.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from urllib.parse import urlsplit

SCHEMAS = Path(__file__).with_name('build_config')
KEYWORDS = {'$schema', 'title', 'type', 'properties', 'required',
            'additionalProperties', 'items', 'minItems', 'uniqueItems',
            'const', 'enum', 'pattern', 'minLength'}


def fail(message):
    raise ValueError(message)


def check_schema(value, schema, path='$'):
    """Check our deliberately small, closed schema vocabulary, failing closed."""
    if set(schema) - KEYWORDS:
        fail('unsupported schema keyword at ' + path)
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str}
    if kind and (kind not in types or type(value) is not types[kind]):
        fail(path + ': expected ' + kind)
    if 'const' in schema and (type(value) is not type(schema['const']) or
                              value != schema['const']):
        fail(path + ': unexpected constant')
    if 'enum' in schema and value not in schema['enum']:
        fail(path + ': unsupported value')
    if kind == 'object':
        if set(schema['required']) - set(value):
            fail(path + ': missing required fields')
        if schema['additionalProperties'] is False and set(value) - set(schema['properties']):
            fail(path + ': unknown fields')
        for key, item in value.items():
            check_schema(item, schema['properties'][key], path + '.' + key)
    if kind == 'array':
        if len(value) < schema.get('minItems', 0):
            fail(path + ': too few items')
        if schema.get('uniqueItems') and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            fail(path + ': duplicate array items')
        for i, item in enumerate(value):
            check_schema(item, schema['items'], path + '[' + str(i) + ']')
    if kind == 'string':
        if len(value) < schema.get('minLength', 0) or value != value.strip():
            fail(path + ': empty or surrounding whitespace')
        if 'pattern' in schema and not re.fullmatch(schema['pattern'], value):
            fail(path + ': invalid format')


def schema(name):
    return json.loads((SCHEMAS / (name + '.schema.json')).read_text())


def os_version(value):
    parts = tuple(int(x) for x in value.split('.'))
    return parts + (0,) * (3 - len(parts))


def normalized(name):
    return re.sub(r'[-_.]+', '-', name).lower()


def validate_configuration(release, lock):
    """Structural and cross-manifest validation only, never grants approval."""
    check_schema(release, schema('release'))
    check_schema(lock, schema('dependencies'))
    target = release['minimum_macos']
    if os_version(target) < (26, 0, 0):
        fail('minimum macOS below current payload support scope')
    # Canonical spelling prevents different env/compiler interpretations.
    if lock['deployment_target'] != target or lock['environment']['MACOSX_DEPLOYMENT_TARGET'] != target:
        fail('contradictory deployment targets')
    if lock['compiler_target'] != 'arm64-apple-macos' + target:
        fail('contradictory compiler target')
    if lock['source_snapshot_sha256'] != release['source_snapshot_sha256']:
        fail('source snapshot mismatch')
    if len(set(release['source_snapshot_sha256'])) == 1:
        fail('placeholder source snapshot checksum')
    # Identifiers are independently explicit; do not invent a namespace relation.
    entries, names, versions, filenames = {}, set(), {}, set()
    for dep in lock['dependencies']:
        name = normalized(dep['name'])
        key = (dep['kind'], name)
        if dep['id'] in entries or key in names or dep['filename'].casefold() in filenames:
            fail('duplicate dependency or cache filename')
        entries[dep['id']] = dep
        names.add(key)
        filenames.add(dep['filename'].casefold())
        if name in versions and versions[name] != dep['version']:
            fail('inconsistent versions for ' + name)
        versions[name] = dep['version']
        if len(set(dep['sha256'])) == 1:
            fail('placeholder checksum')
        if any(ord(char) <= 32 or ord(char) == 127 for char in dep['url']):
            fail('dependency URL contains whitespace/control characters')
        url = urlsplit(dep['url'])
        if (url.scheme != 'https' or not url.hostname or url.username is not None or
                url.password is not None or url.query or url.fragment):
            fail('dependency URL must be credential-free HTTPS without query/fragment')
        if dep['kind'] == 'source-archive':
            if dep['architecture'] != 'any' or 'minimum_macos' in dep:
                fail('source archive must be architecture-independent')
        elif dep['kind'] == 'python-package' and dep['architecture'] == 'any':
            if not dep['filename'].endswith('-none-any.whl') or 'minimum_macos' in dep:
                fail('architecture-independent Python input must be a pure wheel')
        else:
            if dep['architecture'] != 'arm64' or 'minimum_macos' not in dep:
                fail('native dependency requires ARM64 and explicit minimum macOS')
            if os_version(dep['minimum_macos']) > os_version(target):
                fail('dependency minimum macOS exceeds deployment target')
        if dep['kind'] == 'python-package':
            wheel = re.fullmatch(r'([A-Za-z0-9_.]+)-([A-Za-z0-9_.+!]+)(?:-[0-9][A-Za-z0-9_]*)?-([A-Za-z0-9_.]+)-([A-Za-z0-9_.]+)-([A-Za-z0-9_.]+)\.whl', dep['filename'])
            if not wheel or normalized(wheel[1]) != name or wheel[2] != dep['version']:
                fail('wheel name/version inconsistent with dependency')
            if dep['architecture'] == 'arm64':
                tags = wheel[5].split('.')
                for tag in tags:
                    m = re.fullmatch(r'macosx_([0-9]+)_([0-9]+)_arm64', tag)
                    if not m or (int(m[1]), int(m[2]), 0) > os_version(target):
                        fail('wheel platform incompatible with target')
    for dep in entries.values():
        if any(x not in entries for x in dep['requires']):
            fail('unknown dependency reference')
    visiting, done = set(), set()

    def visit(key):
        if key in visiting:
            fail('dependency cycle')
        if key in done:
            return
        visiting.add(key)
        for child in entries[key]['requires']:
            visit(child)
        visiting.remove(key)
        done.add(key)

    for key in entries:
        visit(key)
    for role, key in lock['toolchain'].items():
        if key not in entries:
            fail('missing toolchain dependency: ' + role)
        dep = entries[key]
        expected = 'python-package' if role == 'pyinstaller' else 'toolchain'
        if dep['kind'] != expected:
            fail('incorrect toolchain kind: ' + role)
    python = entries[lock['toolchain']['python']]
    match = re.fullmatch(r'3\.([0-9]+)\.[0-9]+', python['version'])
    if not match:
        fail('toolchain requires an exact Python 3 version')
    minor = int(match[1])
    for dep in entries.values():
        if dep['kind'] != 'python-package':
            continue
        tags = dep['filename'].removesuffix('.whl').split('-')[-3:]
        python_tags, abi, _ = tags
        compatible = 'py3' in python_tags.split('.') and abi == 'none'
        compatible |= python_tags == 'cp3' + str(minor) and abi in ('none', 'cp3' + str(minor), 'abi3')
        old = re.fullmatch(r'cp3([0-9]+)', python_tags)
        compatible |= bool(old and abi == 'abi3' and 2 <= int(old[1]) <= minor)
        if not compatible:
            fail('wheel Python/ABI tags incompatible with locked interpreter')
        if dep['architecture'] == 'arm64':
            for tag in tags[2].split('.'):
                m = re.fullmatch(r'macosx_([0-9]+)_([0-9]+)_arm64', tag)
                if (int(m[1]), int(m[2]), 0) > os_version(dep['minimum_macos']):
                    fail('wheel tag contradicts declared dependency minimum')
    sdk = entries[lock['toolchain']['sdk']]
    if not re.fullmatch(r'[0-9]+\.[0-9]+(?:\.[0-9]+)?', sdk['version']) or os_version(sdk['version']) < os_version(target):
        fail('SDK version older than deployment target or malformed')
    return {'status': 'STRUCTURALLY_VALID_UNAPPROVED', 'architecture': 'arm64',
            'deployment_target': target, 'dependencies': len(entries),
            'build_authorized': False}


def read_regular(path):
    """Read a regular non-symlink leaf without executing it; detect in-read change."""
    path = Path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            fail('input is not a regular file')
        data = stream.read(2 * 1024 * 1024 + 1)
        if len(data) > 2 * 1024 * 1024:
            fail('JSON input exceeds 2 MiB limit')
        after = os.fstat(stream.fileno())
        if (before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            fail('input changed while reading')
    return data


def load_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                fail('duplicate JSON key: ' + key)
            result[key] = value
        return result

    def bad_constant(value):
        fail('non-JSON constant: ' + value)

    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad_constant)


def check_authorization(authorization, release_bytes, lock_bytes):
    """Match review record only; authenticity/authority require external review."""
    check_schema(authorization, schema('authorization'))
    for key, data in [('release_sha256', release_bytes), ('lock_sha256', lock_bytes)]:
        if authorization[key] != hashlib.sha256(data).hexdigest():
            fail('authorization digest mismatch: ' + key)


def metadata_preview(release):
    """Return a pure data mapping for future generation; never writes metadata."""
    check_schema(release, schema('release'))
    return {'info_plist': {'CFBundleShortVersionString': release['product_version'],
                           'CFBundleVersion': release['build_number'],
                           'CFBundleIdentifier': release['application_identifier'],
                           'LSMinimumSystemVersion': release['minimum_macos']},
            'gui_version': release['product_version'],
            'version_resource': release['product_version'],
            'package_identifier': release['package_identifier'],
            'package_version': release['product_version']}


def check_metadata_preview(release, preview):
    if preview != metadata_preview(release):
        fail('metadata preview contradicts central release manifest')


def verify_cache(lock, directory):
    """Hash already-acquired flat cache files through an anchored directory fd."""
    check_schema(lock, schema('dependencies'))
    root_fd = os.open(directory, os.O_RDONLY | os.O_NOFOLLOW | os.O_DIRECTORY)
    try:
        for dep in lock['dependencies']:
            fd = os.open(dep['filename'], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                         dir_fd=root_fd)
            with os.fdopen(fd, 'rb') as stream:
                before = os.fstat(stream.fileno())
                if not stat.S_ISREG(before.st_mode):
                    fail('cache input is not a regular file')
                digest = hashlib.sha256()
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
                after = os.fstat(stream.fileno())
                if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                        after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                    fail('cache input changed while reading')
                if digest.hexdigest() != dep['sha256']:
                    fail('cache checksum mismatch: ' + dep['id'])
    finally:
        os.close(root_fd)
    return len(lock['dependencies'])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', required=True)
    parser.add_argument('--lock', required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--check-draft', action='store_true')
    mode.add_argument('--authorization', help='External configuration-review record; never build approval')
    parser.add_argument('--cache', help='Optional already-acquired flat cache to read/hash')
    parser.add_argument('--metadata-preview', help='Optional generated-metadata JSON to compare; never written')
    args = parser.parse_args(argv)
    try:
        release_bytes, lock_bytes = read_regular(args.release), read_regular(args.lock)
        release, lock = load_json(release_bytes), load_json(lock_bytes)
        result = validate_configuration(release, lock)
        if not args.check_draft:
            if not args.authorization:
                fail('unapproved configuration: external review record required; --check-draft checks syntax only')
            check_authorization(load_json(read_regular(args.authorization)), release_bytes, lock_bytes)
            result['status'] = 'CONFIGURATION_REVIEW_RECORD_MATCHED'
        if args.metadata_preview:
            check_metadata_preview(release, load_json(read_regular(args.metadata_preview)))
            result['metadata_preview_verified'] = True
        if args.cache:
            result['cache_files_verified'] = verify_cache(lock, args.cache)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, RecursionError) as error:
        print(json.dumps({'status': 'REJECTED', 'error': str(error), 'build_authorized': False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
