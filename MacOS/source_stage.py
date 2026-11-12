"""Verify and stage a pinned local Git snapshot without checking out or running it.

Only regular Git blobs and trees are supported. No fetch, filters, patches,
submodule initialization, source imports, installer or build execution occurs.
"""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import unicodedata

PINNED_REVISION = 'd86c1891b4e1aced7ce84b910d6fba17025bd87c'
MACOS_ROOT = Path(__file__).absolute().parent
MAX_OBJECT_BYTES = 128 * 1024 * 1024
MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024
MAX_ENTRIES = 50000
MAX_DEPTH = 64
MAX_MANIFEST_BYTES = 32 * 1024 * 1024


class StagingError(ValueError):
    """An integrity, path, format or staging contract was refused."""


def git_id(kind, data):
    header = (kind + ' ' + str(len(data))).encode('ascii') + b'\0'
    return hashlib.sha1(header + data).hexdigest()


def check_id(value):
    if not isinstance(value, str) or re.fullmatch('[0-9a-f]{40}', value) is None:
        raise StagingError('Expected a full lowercase SHA-1 Git object ID')
    return value


def component(value):
    if (not isinstance(value, str) or not value or value in ('.', '..')
            or any(c in value for c in '/\\:') or value.endswith((' ', '.'))
            or value.casefold() == '.git' or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise StagingError('Unsafe source path component')
    value.encode('utf-8', errors='strict')
    return value


def commit_tree(data, revision):
    if len(data) > 2 * 1024 * 1024 or git_id('commit', data) != revision:
        raise StagingError('Commit content does not match the pinned revision')
    first, separator, rest = data.partition(b'\n')
    if not separator or not first.startswith(b'tree ') or b'\n\n' not in data:
        raise StagingError('Malformed Git commit')
    try:
        return check_id(first[5:].decode('ascii'))
    except UnicodeError as error:
        raise StagingError('Malformed commit tree ID') from error


def directory(path, private=False):
    """Reject aliases and unsafe directory custody before pathname operations."""
    path = Path(path).absolute()
    for current in (path, *path.parents):
        info = current.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid not in (0, os.getuid()):
            raise StagingError('Untrusted or linked directory: ' + str(current))
        if info.st_mode & 0o022 and not info.st_mode & stat.S_ISVTX:
            raise StagingError('Writable non-sticky directory: ' + str(current))
    if private and (path.stat().st_uid != os.getuid()
                    or stat.S_IMODE(path.stat().st_mode) != 0o700):
        raise StagingError('Staging directories must be user-owned mode 0700')
    return path


@contextmanager
def objects(repository):
    """Read raw Git objects. No checkout, config-dependent filters or network."""
    repository = directory(repository)
    git_dir = repository / '.git' if (repository / '.git').is_dir() else repository
    directory(git_dir)
    directory(git_dir / 'objects')
    git = shutil.which('git')
    if git is None:
        raise StagingError('Git is required for local object inspection')
    environment = {k: os.environ[k] for k in ('PATH', 'SYSTEMROOT') if k in os.environ}
    environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_NO_REPLACE_OBJECTS='1', GIT_OPTIONAL_LOCKS='0',
                       GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1', LC_ALL='C')
    process = subprocess.Popen(
        [git, '--no-replace-objects', '--git-dir=' + str(git_dir), 'cat-file', '--batch'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        env=environment, cwd=repository)
    try:
        def read(oid, expected):
            check_id(oid)
            process.stdin.write(oid.encode('ascii') + b'\n')
            process.stdin.flush()
            header = process.stdout.readline(128).split()
            if len(header) != 3 or header[0] != oid.encode() or header[1] != expected.encode():
                raise StagingError('Missing object or unexpected Git object type: ' + oid)
            try:
                size = int(header[2])
            except ValueError as error:
                raise StagingError('Malformed Git object length') from error
            if not 0 <= size <= MAX_OBJECT_BYTES:
                raise StagingError('Git object exceeds the size limit')
            data = process.stdout.read(size)
            if len(data) != size or process.stdout.read(1) != b'\n':
                raise StagingError('Truncated Git object')
            if git_id(expected, data) != oid:
                raise StagingError('Git object hash mismatch: ' + oid)
            return data
        yield read
    finally:
        process.stdin.close()
        process.stdout.close()
        try:
            result = process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise StagingError('Git object reader did not shut down')
        if result:
            raise StagingError('Git object reader failed')


def inventory(read, tree):
    entries = []
    identities = set()

    def visit(oid, parent, depth):
        if depth > MAX_DEPTH:
            raise StagingError('Source tree exceeds the depth limit')
        raw = read(oid, 'tree')
        position = 0
        siblings = set()
        while position < len(raw):
            end = raw.find(b'\0', position)
            if end < 0 or end + 21 > len(raw):
                raise StagingError('Truncated Git tree entry')
            metadata = raw[position:end].split(b' ', 1)
            if len(metadata) != 2:
                raise StagingError('Malformed Git tree entry')
            try:
                mode = metadata[0].decode('ascii')
                name = component(metadata[1].decode('utf-8'))
            except UnicodeError as error:
                raise StagingError('Non-UTF-8 source path') from error
            if mode not in ('40000', '100644', '100755'):
                raise StagingError('Unsupported Git mode ' + mode + ' (links/submodules are not staged)')
            path = parent + name
            identity = unicodedata.normalize('NFD', path).casefold()
            if name in siblings or identity in identities:
                raise StagingError('Duplicate or case/Unicode-colliding source path: ' + path)
            siblings.add(name)
            identities.add(identity)
            child = raw[end + 1:end + 21].hex()
            entries.append({'path': path, 'mode': mode, 'git_oid': child})
            if len(entries) > MAX_ENTRIES:
                raise StagingError('Source tree exceeds the entry limit')
            if mode == '40000':
                visit(child, path + '/', depth + 1)
            position = end + 21
    visit(tree, '', 0)
    return sorted(entries, key=lambda row: row['path'])


def exclusive(path, data, mode=0o600):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'wb') as stream:
        os.fchmod(stream.fileno(), mode)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def encoded(data):
    return (json.dumps(data, sort_keys=True, indent=2, ensure_ascii=True) + '\n').encode()


def stage_base(create=False):
    root = directory(MACOS_ROOT)
    for leaf in ('.migration-work', 'source-staging', PINNED_REVISION):
        root = root / leaf
        if create:
            try:
                root.mkdir(mode=0o700)
            except FileExistsError:
                pass
        if root.exists() or root.is_symlink():
            directory(root, private=True)
    return root


def run_path(run_id):
    if (not isinstance(run_id, str) or re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,63}', run_id) is None):
        raise StagingError('Run ID must be one portable 1–64 character leaf')
    return Path(MACOS_ROOT) / '.migration-work/source-staging' / PINNED_REVISION / run_id


def manifest_tree(manifest):
    """Reconstruct every Git tree to bind the complete inventory to the commit."""
    if (type(manifest.get('schema_version')) is not int or manifest['schema_version'] != 1
            or manifest.get('revision') != PINNED_REVISION):
        raise StagingError('Unexpected source manifest version or revision')
    try:
        commit = bytes.fromhex(manifest['commit_hex'])
    except (ValueError, TypeError) as error:
        raise StagingError('Malformed manifest commit') from error
    root = commit_tree(commit, PINNED_REVISION)
    if manifest['root_tree'] != root:
        raise StagingError('Manifest root tree differs from the pinned commit')
    children = {'': []}
    declared = {}
    identities = set()
    entries = manifest['entries']
    if not isinstance(entries, list) or len(entries) > MAX_ENTRIES:
        raise StagingError('Invalid source manifest entries')
    for row in entries:
        path = row['path']
        if not isinstance(path, str):
            raise StagingError('Invalid manifest path')
        parts = path.split('/')
        if len(parts) > MAX_DEPTH + 1:
            raise StagingError('Manifest path too deep')
        for part in parts:
            component(part)
        identity = unicodedata.normalize('NFD', path).casefold()
        if identity in identities:
            raise StagingError('Duplicate manifest path')
        identities.add(identity)
        mode = row['mode']
        if mode not in ('40000', '100644', '100755'):
            raise StagingError('Unsupported manifest mode')
        check_id(row['git_oid'])
        parent = '/'.join(parts[:-1])
        children.setdefault(parent, []).append(row)
        if mode == '40000':
            children.setdefault(path, [])
            declared[path] = row['git_oid']
        else:
            if (type(row.get('size')) is not int or not 0 <= row['size'] <= MAX_OBJECT_BYTES
                    or re.fullmatch('[0-9a-f]{64}', row.get('sha256', '')) is None):
                raise StagingError('Invalid manifest file digest/size')
    if set(children) != {'', *declared}:
        raise StagingError('Missing directory or file/directory path collision')
    for parent, rows in children.items():
        def sort_key(row):
            return row['path'].rsplit('/', 1)[-1].encode() + (b'/' if row['mode'] == '40000' else b'')
        raw = b''.join(row['mode'].encode() + b' ' + row['path'].rsplit('/', 1)[-1].encode()
                       + b'\0' + bytes.fromhex(row['git_oid']) for row in sorted(rows, key=sort_key))
        if git_id('tree', raw) != (root if not parent else declared[parent]):
            raise StagingError('Manifest inventory does not reconstruct the pinned Git tree')
    return entries


def read_file(path, limit):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
                or before.st_uid != os.getuid() or before.st_size > limit):
            raise StagingError('Unsafe or oversized staged file: ' + str(path))
        data = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
        if (len(data) > limit or (before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
                != (after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns)):
            raise StagingError('Staged file changed during inspection')
    return data, stat.S_IMODE(before.st_mode)


def verify_trees(run, manifest):
    entries = manifest_tree(manifest)
    expected = {row['path']: row for row in entries}
    for name in ('pristine-source', 'candidate-source'):
        root = directory(run / name, private=True)
        found = {}
        def walk(parent):
            for item in parent.iterdir():
                relative = item.relative_to(root).as_posix()
                info = item.lstat()
                found[relative] = info
                if stat.S_ISDIR(info.st_mode):
                    directory(item, private=True)
                    walk(item)
        walk(root)
        if set(found) != set(expected):
            raise StagingError('Staged tree inventory differs: ' + name)
        total = 0
        for path, row in expected.items():
            target = root / path
            if row['mode'] == '40000':
                directory(target, private=True)
                continue
            data, mode = read_file(target, row['size'])
            if (len(data) != row['size'] or mode != int(row['mode'], 8) & 0o777
                    or hashlib.sha256(data).hexdigest() != row['sha256']
                    or git_id('blob', data) != row['git_oid']):
                raise StagingError('Staged file integrity mismatch: ' + path)
            total += len(data)
        if total > MAX_TOTAL_BYTES:
            raise StagingError('Staged tree exceeds the total size limit')
    return {'status': 'VERIFIED_SOURCE_ONLY', 'revision': PINNED_REVISION,
            'root_tree': manifest['root_tree'], 'files': sum(row['mode'] != '40000' for row in entries)}


def stage_source(repository, run_id):
    run = run_path(run_id)
    stage_base()
    # Refuse reuse before consulting source or allocating any new output.
    if run.exists() or run.is_symlink():
        raise StagingError('Refusing existing run directory; select a fresh run ID')
    with objects(repository) as read:
        commit = read(PINNED_REVISION, 'commit')
        tree = commit_tree(commit, PINNED_REVISION)
        entries = inventory(read, tree)
        # Verify all blobs and bounds before any staging directory allocation.
        total = 0
        for row in entries:
            if row['mode'] != '40000':
                data = read(row['git_oid'], 'blob')
                row.update(size=len(data), sha256=hashlib.sha256(data).hexdigest())
                total += len(data)
                if total > MAX_TOTAL_BYTES:
                    raise StagingError('Source exceeds the total size limit')
        manifest = {'schema_version': 1, 'revision': PINNED_REVISION,
                    'root_tree': tree, 'commit_hex': commit.hex(), 'entries': entries}
        manifest_tree(manifest)
        stage_base(create=True)
        run.mkdir(mode=0o700)  # Atomic no-overwrite allocation, including competing callers.
        try:
            directory(run, private=True)
            for name in ('pristine-source', 'candidate-source'):
                (run / name).mkdir(mode=0o700)
            for row in entries:
                for name in ('pristine-source', 'candidate-source'):
                    target = run / name / row['path']
                    directory(target.parent, private=True)
                    if row['mode'] == '40000':
                        target.mkdir(mode=0o700)
                    else:
                        data = read(row['git_oid'], 'blob')
                        if len(data) != row['size'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                            raise StagingError('Source object changed during staging')
                        exclusive(target, data, int(row['mode'], 8) & 0o777)
            result = verify_trees(run, manifest)
            manifest_bytes = encoded(manifest)
            exclusive(run / 'manifest.json', manifest_bytes)
            result['manifest_sha256'] = hashlib.sha256(manifest_bytes).hexdigest()
        except BaseException:
            # Retain partial outputs for diagnosis. Never recursively remove source/output.
            if run.is_dir() and not run.is_symlink():
                exclusive(run / 'FAILED.json', encoded({'status': 'FAILED', 'retry_requires_new_run': True}))
            raise
    # Completion is published only after the Git reader also exits successfully.
    exclusive(run / 'COMPLETE.json', encoded(result))
    return verify_stage(run_id)


def json_record(data):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise StagingError('Duplicate JSON key')
            result[key] = value
        return result

    def invalid_constant(value):
        raise StagingError('Invalid JSON constant: ' + value)

    result = json.loads(data, object_pairs_hook=unique_pairs, parse_constant=invalid_constant)
    if not isinstance(result, dict):
        raise StagingError('Expected a JSON object record')
    return result


def verify_stage(run_id):
    run = directory(run_path(run_id), private=True)
    if {p.name for p in run.iterdir()} != {'pristine-source', 'candidate-source', 'manifest.json', 'COMPLETE.json'}:
        raise StagingError('Incomplete, failed or unexpected staging output')
    raw, mode = read_file(run / 'manifest.json', MAX_MANIFEST_BYTES)
    completion, complete_mode = read_file(run / 'COMPLETE.json', 4096)
    if mode != 0o600 or complete_mode != 0o600:
        raise StagingError('Incorrect manifest/completion permissions')
    manifest = json_record(raw)
    result = verify_trees(run, manifest)
    result['manifest_sha256'] = hashlib.sha256(raw).hexdigest()
    if json_record(completion) != result:
        raise StagingError('Completion record differs from verified contents')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--source-repository', type=Path, help='Already available local Git repository')
    action.add_argument('--verify', action='store_true', help='Recheck both unchanged staged trees')
    args = parser.parse_args(argv)
    try:
        result = verify_stage(args.run_id) if args.verify else stage_source(args.source_repository, args.run_id)
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0
    except (StagingError, OSError, UnicodeError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({'status': 'REFUSED', 'error': str(error)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
