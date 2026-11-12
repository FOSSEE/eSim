"""Synthetic build-configuration tests: no tools, dependencies or installers run."""
import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

from MacOS import build_config_validate as validate


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fixtures():
    # Deliberately synthetic test-only numbers/identifiers, never release choices.
    release = {'schema_version': 1, 'status': 'proposed', 'product_version': '7.8.9',
               'build_number': '123', 'application_identifier': 'org.example.esim',
               'package_identifier': 'org.example.esim.pkg', 'minimum_macos': '26.0',
               'architecture': 'arm64', 'source_snapshot_sha256': digest(b'synthetic source')}
    deps = []
    roles = {}
    for role in ('sdk', 'clang', 'clangxx', 'linker', 'ar', 'ranlib', 'python', 'pyinstaller'):
        version = {'sdk': '26.2', 'python': '3.14.0', 'pyinstaller': '9.8.7'}.get(role, '17.0.0')
        name = 'synthetic-' + role
        filename = name + '.bin'
        kind, arch = 'toolchain', 'arm64'
        if role == 'pyinstaller':
            filename, kind, arch = name.replace('-', '_') + '-' + version + '-py3-none-any.whl', 'python-package', 'any'
        d = {'id': role, 'name': name, 'kind': kind, 'version': version,
             'architecture': arch, 'filename': filename,
             'url': 'https://example.invalid/' + filename,
             'sha256': digest(('fixture:' + role).encode()), 'requires': []}
        if arch == 'arm64':
            d['minimum_macos'] = '26.0'
        deps.append(d)
        roles[role] = role
    lock = {'schema_version': 1, 'status': 'proposed',
            'source_snapshot_sha256': release['source_snapshot_sha256'],
            'architecture': 'arm64', 'deployment_target': '26.0',
            'compiler_target': 'arm64-apple-macos26.0',
            'environment': {'MACOSX_DEPLOYMENT_TARGET': '26.0',
                            'ARCHFLAGS': '-arch arm64', 'SDKROOT': '@locked-sdk@'},
            'toolchain': roles, 'dependencies': deps}
    return release, lock


class BuildConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.release, self.lock = fixtures()
        self.temp = tempfile.TemporaryDirectory(prefix='esim-build-config-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def check(self):
        return validate.validate_configuration(self.release, self.lock)

    def rejects(self):
        with self.assertRaises(ValueError):
            self.check()

    def cli(self, *extra):
        r, l = self.root / 'release.json', self.root / 'lock.json'
        r.write_text(json.dumps(self.release)); l.write_text(json.dumps(self.lock))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = validate.main(['--release', str(r), '--lock', str(l), *extra])
        return code, json.loads(output.getvalue())

    def test_complete_synthetic_draft_is_never_build_authorization(self):
        self.assertEqual(self.check()['status'], 'STRUCTURALLY_VALID_UNAPPROVED')
        self.assertFalse(self.check()['build_authorized'])

    def test_every_required_release_field(self):
        original = copy.deepcopy(self.release)
        for key in original:
            with self.subTest(field=key):
                self.release = copy.deepcopy(original); del self.release[key]; self.rejects()

    def test_every_required_lock_field(self):
        original = copy.deepcopy(self.lock)
        for key in original:
            with self.subTest(field=key):
                self.lock = copy.deepcopy(original); del self.lock[key]; self.rejects()

    def test_unset_checked_in_proposals_rejected(self):
        for name, kind in [('release.proposed.json', 'release'), ('dependencies.proposed.json', 'dependencies')]:
            with self.subTest(file=name), self.assertRaises(ValueError):
                validate.check_schema(json.loads((validate.SCHEMAS / name).read_text()), validate.schema(kind))

    def test_product_version_format(self):
        for value in ['2.5', '01.2.3', '1.2.3-beta', '', None, 2.5, '1.2.3\n', '１.2.3']:
            with self.subTest(value=value):
                self.release['product_version'] = value; self.rejects()

    def test_build_number_format(self):
        for value in ['0', '01', '10000', '1.2', '-1', 1, True, None]:
            with self.subTest(value=value):
                self.release['build_number'] = value; self.rejects()

    def test_identifier_format(self):
        for field in ('application_identifier', 'package_identifier'):
            original = self.release[field]
            for value in ['eSim', 'org..esim', 'org.example/eSim', ' org.example.esim', None]:
                with self.subTest(field=field, value=value):
                    self.release[field] = value; self.rejects()
            self.release[field] = original

    def test_central_metadata_mapping_and_contradictory_identifiers(self):
        preview = validate.metadata_preview(self.release)
        validate.check_metadata_preview(self.release, preview)
        for key in ('CFBundleIdentifier', 'CFBundleVersion', 'CFBundleShortVersionString', 'LSMinimumSystemVersion'):
            changed = copy.deepcopy(preview); changed['info_plist'][key] = 'different'
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate.check_metadata_preview(self.release, changed)
        for key in ('gui_version', 'version_resource', 'package_version', 'package_identifier'):
            changed = copy.deepcopy(preview); changed[key] = 'different'
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate.check_metadata_preview(self.release, changed)

    def test_unsupported_architectures(self):
        for key in ('release', 'lock'):
            data = getattr(self, key)
            for value in ('x86_64', 'universal2', 'ARM64', None):
                with self.subTest(manifest=key, value=value):
                    data['architecture'] = value; self.rejects()
            data['architecture'] = 'arm64'

    def test_unknown_fields_and_self_approval(self):
        for target in (self.release, self.lock, self.lock['environment'], self.lock['dependencies'][0]):
            target['approved'] = True; self.rejects(); del target['approved']
        self.release['status'] = 'approved'; self.rejects()

    def test_schema_version_is_not_boolean(self):
        self.release['schema_version'] = True; self.rejects()

    def test_minimum_os_and_explicit_target_controls(self):
        for field, value in [('minimum_macos', '25.0'), ('minimum_macos', '26'), ('minimum_macos', '26.00')]:
            self.release[field] = value; self.rejects()
        self.release['minimum_macos'] = '26.0'
        self.lock['deployment_target'] = '27.0'; self.rejects()
        self.lock['deployment_target'] = '26.0'
        self.lock['compiler_target'] = 'x86_64-apple-macos26.0'; self.rejects()
        self.lock['compiler_target'] = 'arm64-apple-macos26.0'
        self.lock['environment']['MACOSX_DEPLOYMENT_TARGET'] = '27.0'; self.rejects()

    def test_source_snapshot_mismatch(self):
        self.lock['source_snapshot_sha256'] = digest(b'other source'); self.rejects()

    def test_missing_malformed_placeholder_checksums(self):
        dep = self.lock['dependencies'][0]
        original = dep['sha256']
        del dep['sha256']; self.rejects()
        for value in ['', 'a' * 63, 'z' * 64, '0' * 64, original.upper(), None]:
            with self.subTest(value=value):
                dep['sha256'] = value; self.rejects()

    def test_duplicate_dependency_ids_names_and_cache_filenames(self):
        dep = copy.deepcopy(self.lock['dependencies'][0])
        self.lock['dependencies'].append(dep); self.rejects()
        dep['id'] = 'other'; self.rejects()
        dep['filename'] = 'other.bin'; self.rejects()
        dep['name'] = 'different'; dep['filename'] = self.lock['dependencies'][0]['filename']; self.rejects()
        dep['filename'] = dep['filename'].upper(); self.rejects()

    def test_normalized_python_name_duplicates(self):
        dep = copy.deepcopy(self.lock['dependencies'][-1]); dep['id'] = 'other'
        dep['name'] = 'Synthetic_Pyinstaller'; dep['filename'] = 'other.whl'
        self.lock['dependencies'].append(dep); self.rejects()

    def test_inconsistent_source_and_binary_versions(self):
        dep = copy.deepcopy(self.lock['dependencies'][0])
        dep.update(id='source', kind='source-archive', architecture='any', version='99.0', filename='source.tar.xz')
        del dep['minimum_macos']; self.lock['dependencies'].append(dep); self.rejects()

    def test_unpinned_versions(self):
        for value in ['latest', 'master', '>=1.0', '1.*', '', None]:
            self.lock['dependencies'][0]['version'] = value; self.rejects()

    def test_native_dependency_requires_architecture_and_minimum(self):
        dep = self.lock['dependencies'][0]
        dep['architecture'] = 'any'; self.rejects(); dep['architecture'] = 'arm64'
        del dep['minimum_macos']; self.rejects(); dep['minimum_macos'] = '27.0'; self.rejects()

    def test_source_archive_and_upstream_binary_formats(self):
        source = copy.deepcopy(self.lock['dependencies'][0])
        source.update(id='source', name='synthetic-source', kind='source-archive', architecture='any', filename='source.tar.xz')
        del source['minimum_macos']; self.lock['dependencies'].append(source)
        binary = copy.deepcopy(self.lock['dependencies'][1])
        binary.update(id='binary', name='synthetic-binary', kind='upstream-binary', filename='upstream.zip')
        self.lock['dependencies'].append(binary); self.check()
        source['architecture'] = 'arm64'; self.rejects()

    def test_unsafe_urls_and_paths(self):
        dep = self.lock['dependencies'][0]; original = dep['url']
        for value in ['http://example.invalid/a', 'file:///a', 'https://user:pass@example.invalid/a', 'https://example.invalid/a?token=x', 'https://example.invalid/a#x', 'https://exam\nple.invalid/a']:
            dep['url'] = value; self.rejects()
        dep['url'] = original
        for value in ['../secret', '/tmp/secret', 'sub/file', '..', '.']:
            dep['filename'] = value; self.rejects()

    def test_dependency_graph_missing_refs_cycles_and_duplicate_edges(self):
        a, b = self.lock['dependencies'][:2]
        a['requires'] = ['missing']; self.rejects()
        a['requires'] = [b['id']]; b['requires'] = [a['id']]; self.rejects()
        b['requires'] = []; a['requires'] = [b['id'], b['id']]; self.rejects()

    def test_missing_toolchain_and_wrong_kind(self):
        self.lock['toolchain']['clang'] = 'unknown'; self.rejects()
        self.lock['toolchain']['clang'] = 'pyinstaller'; self.rejects()

    def test_sdk_version_cannot_be_older_than_floor(self):
        self.lock['dependencies'][0]['version'] = '25.0'; self.rejects()

    def test_wheel_name_version_and_python_abi(self):
        dep = self.lock['dependencies'][-1]
        for value in ['other-9.8.7-py3-none-any.whl', 'synthetic_pyinstaller-1.0-py3-none-any.whl', 'synthetic_pyinstaller-9.8.7-cp313-cp313-macosx_26_0_arm64.whl']:
            dep['filename'] = value; dep['architecture'] = 'arm64'; dep['minimum_macos'] = '26.0'; self.rejects()

    def test_native_wheel_target_and_interpreter_consistency(self):
        dep = self.lock['dependencies'][-1]
        dep.update(filename='synthetic_pyinstaller-9.8.7-cp314-cp314-macosx_26_0_arm64.whl', architecture='arm64', minimum_macos='26.0')
        self.check()
        dep['filename'] = dep['filename'].replace('arm64', 'x86_64'); self.rejects()
        dep['filename'] = 'synthetic_pyinstaller-9.8.7-cp314-cp314-macosx_27_0_arm64.whl'; self.rejects()
        dep['filename'] = 'synthetic_pyinstaller-9.8.7-cp314-cp314-macosx_26_0_arm64.whl'
        dep['minimum_macos'] = '11.0'; self.rejects()

    def test_strict_json(self):
        for data in [b'{"x":1,"x":2}', b'{"x": NaN}', b'{"x": Infinity}', b'not json']:
            with self.subTest(data=data), self.assertRaises(ValueError):
                validate.load_json(data)

    def test_unknown_schema_keywords_fail_closed(self):
        with self.assertRaises(ValueError):
            validate.check_schema('abc', {'type': 'string', 'unsupported': True})

    def test_cli_requires_external_authorization_by_default(self):
        code, output = self.cli(); self.assertEqual(code, 2)
        self.assertIn('unapproved', output['error']); self.assertFalse(output['build_authorized'])
        code, output = self.cli('--check-draft'); self.assertEqual(code, 0)
        self.assertEqual(output['status'], 'STRUCTURALLY_VALID_UNAPPROVED')

    def test_external_record_binds_both_exact_inputs_only(self):
        self.cli('--check-draft')
        r = {'schema_version': 1, 'scope': 'configuration-review-only',
             'release_sha256': digest((self.root / 'release.json').read_bytes()),
             'lock_sha256': digest((self.root / 'lock.json').read_bytes()),
             'approved_by': 'SYNTHETIC TEST REVIEWER', 'reference': 'TEST ONLY'}
        path = self.root / 'review.json'; path.write_text(json.dumps(r))
        code, output = self.cli('--authorization', str(path)); self.assertEqual(code, 0)
        self.assertFalse(output['build_authorized'])
        self.release['build_number'] = '124'
        code, _ = self.cli('--authorization', str(path)); self.assertEqual(code, 2)
        self.release['build_number'] = '123'; self.lock['dependencies'][0]['url'] += '/changed'
        code, _ = self.cli('--authorization', str(path)); self.assertEqual(code, 2)
        r['scope'] = 'build'; path.write_text(json.dumps(r))
        code, _ = self.cli('--authorization', str(path)); self.assertEqual(code, 2)

    def test_cli_cache_and_metadata_preview_are_read_only(self):
        for dep in self.lock['dependencies']:
            (self.root / dep['filename']).write_bytes(('fixture:' + dep['id']).encode())
        preview = self.root / 'preview.json'
        preview.write_text(json.dumps(validate.metadata_preview(self.release)))
        before = {p.name: digest(p.read_bytes()) for p in self.root.iterdir()}
        code, result = self.cli('--check-draft', '--cache', str(self.root),
                                '--metadata-preview', str(preview))
        self.assertEqual(code, 0)
        self.assertEqual(result['cache_files_verified'], 8)
        self.assertTrue(result['metadata_preview_verified'])
        self.assertFalse(result['build_authorized'])
        self.assertEqual(before, {p.name: digest(p.read_bytes()) for p in self.root.iterdir()
                                  if p.name not in ('release.json', 'lock.json')})
        preview.write_text('{}')
        code, _ = self.cli('--check-draft', '--metadata-preview', str(preview))
        self.assertEqual(code, 2)

    def test_cache_verification_detects_mutation_and_missing_file(self):
        for dep in self.lock['dependencies']:
            data = ('fixture:' + dep['id']).encode(); (self.root / dep['filename']).write_bytes(data)
        self.assertEqual(validate.verify_cache(self.lock, self.root), 8)
        p = self.root / self.lock['dependencies'][0]['filename']; p.write_bytes(b'changed')
        with self.assertRaises(ValueError): validate.verify_cache(self.lock, self.root)
        p.unlink()
        with self.assertRaises(OSError): validate.verify_cache(self.lock, self.root)

    def test_symlink_directory_and_fifo_inputs_rejected(self):
        target = self.root / 'target'; target.write_bytes(b'{}')
        link = self.root / 'link'; link.symlink_to(target)
        for path in (link, self.root):
            with self.subTest(path=path), self.assertRaises((ValueError, OSError)):
                validate.read_regular(path)
        fifo = self.root / 'fifo'; os.mkfifo(fifo)
        with self.assertRaises(ValueError): validate.read_regular(fifo)
        cache_link = self.root / 'cache-link'; cache_link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(OSError): validate.verify_cache(self.lock, cache_link)
        first = self.root / self.lock['dependencies'][0]['filename']; first.symlink_to(target)
        with self.assertRaises(OSError): validate.verify_cache(self.lock, self.root)

    def test_oversized_manifest_rejected(self):
        p = self.root / 'large.json'; p.write_bytes(b' ' * (2 * 1024 * 1024 + 1))
        with self.assertRaises(ValueError): validate.read_regular(p)


if __name__ == '__main__':
    unittest.main()
