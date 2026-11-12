"""Synthetic Git-object responses only. No Git commit, checkout or app execution."""
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from MacOS import source_stage as stage


class FakeGit:
    """In-memory cat-file protocol; no executable is started."""
    def __init__(self, objects):
        self.objects = objects
        self.stdout = io.BytesIO()
        self.stdin = self

    def write(self, request):
        oid = request.decode().strip()
        if oid not in self.objects:
            reply = (oid + ' missing\n').encode()
        else:
            kind, content = self.objects[oid]
            reply = f'{oid} {kind} {len(content)}\n'.encode() + content + b'\n'
        self.stdout = io.BytesIO(reply)
        return len(request)

    def flush(self):
        pass

    def close(self):
        pass

    def wait(self, timeout=None):
        return 0


class SourceStageTests(unittest.TestCase):
    def setUp(self):
        # Only new disposable fixtures under the integration clone's ignored area.
        self.fixture_parent = Path(stage.MACOS_ROOT) / '.migration-work'
        self.fixture_parent.mkdir(mode=0o700, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='synthetic-', dir=self.fixture_parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.macos = self.root / 'packaging/MacOS'
        self.macos.mkdir(parents=True, mode=0o700)
        (self.macos / 'src').mkdir()
        self.sentinel = self.macos / 'src/existing.py'
        self.sentinel.write_bytes(b'existing official source, never replaced\n')
        self.repository = self.root / 'source-repository'
        (self.repository / '.git/objects').mkdir(parents=True, mode=0o700)
        self.pool = {}
        test_tree = self.tree([('100644', 'test_example.py', self.blob(b'raise RuntimeError("do not execute")\n'))])
        self.tree_oid = self.tree([
            ('100644', '.gitattributes', self.blob(b'/tests/ export-ignore\n')),
            ('100644', 'VERSION', self.blob(b'2.6\n')),
            ('100644', 'requirements.txt', self.blob(b'fixture-only\n')),
            ('100755', 'script.py', self.blob(b'raise RuntimeError("never launch")\n')),
            ('40000', 'tests', test_tree)])
        self.commit = self.make_commit(self.tree_oid)
        self.addCleanup(mock.patch.stopall)
        mock.patch.object(stage, 'MACOS_ROOT', self.macos).start()
        mock.patch.object(stage, 'PINNED_REVISION', self.commit).start()
        mock.patch.object(stage.shutil, 'which', return_value='/synthetic/git').start()
        self.spawn = mock.patch.object(stage.subprocess, 'Popen', side_effect=lambda *a, **k: FakeGit(self.pool)).start()

    def add(self, kind, content):
        oid = stage.git_id(kind, content)
        self.pool[oid] = (kind, content)
        return oid

    def blob(self, data):
        return self.add('blob', data)

    def tree(self, rows):
        rows = sorted(rows, key=lambda r: r[1].encode() + (b'/' if r[0] == '40000' else b''))
        data = b''.join(mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(oid)
                        for mode, name, oid in rows)
        return self.add('tree', data)

    def make_commit(self, tree):
        data = ('tree ' + tree + '\nauthor Synthetic <fixture@example.invalid> 0 +0000\n'
                'committer Synthetic <fixture@example.invalid> 0 +0000\n\nsynthetic data\n').encode()
        return self.add('commit', data)

    def select_tree(self, tree):
        self.tree_oid = tree
        self.commit = self.make_commit(tree)
        stage.PINNED_REVISION = self.commit

    def run_source(self, name='run1'):
        return stage.stage_source(self.repository, name)

    def test_independent_verified_trees_include_export_ignored_developer_files(self):
        result = self.run_source()
        self.assertEqual(result['status'], 'VERIFIED_SOURCE_ONLY')
        self.assertEqual(result['files'], 5)
        run = stage.run_path('run1')
        for tree in ('pristine-source', 'candidate-source'):
            self.assertEqual((run / tree / 'requirements.txt').read_bytes(), b'fixture-only\n')
            self.assertTrue((run / tree / 'tests/test_example.py').is_file())
            self.assertEqual((run / tree / 'script.py').stat().st_mode & 0o777, 0o755)
        left = run / 'pristine-source/VERSION'
        right = run / 'candidate-source/VERSION'
        self.assertNotEqual(left.stat().st_ino, right.stat().st_ino)
        self.assertEqual(self.sentinel.read_bytes(), b'existing official source, never replaced\n')
        self.assertEqual(stage.verify_stage('run1'), result)

    def test_repeatable_manifest_across_fresh_runs(self):
        self.run_source('one')
        self.run_source('two')
        self.assertEqual((stage.run_path('one') / 'manifest.json').read_bytes(),
                         (stage.run_path('two') / 'manifest.json').read_bytes())
        self.assertEqual((stage.run_path('one') / 'COMPLETE.json').read_bytes(),
                         (stage.run_path('two') / 'COMPLETE.json').read_bytes())

    def test_existing_run_is_never_overwritten(self):
        self.run_source()
        before = (stage.run_path('run1') / 'manifest.json').read_bytes()
        self.spawn.reset_mock()
        with self.assertRaisesRegex(stage.StagingError, 'existing run'):
            self.run_source()
        self.spawn.assert_not_called()
        self.assertEqual((stage.run_path('run1') / 'manifest.json').read_bytes(), before)

    def test_competing_allocations_have_one_winner(self):
        def attempt():
            try:
                self.run_source('competing')
                return True
            except (OSError, stage.StagingError):
                return False
        with ThreadPoolExecutor(max_workers=2) as executor:
            self.assertEqual(sorted(executor.map(lambda _: attempt(), range(2))), [False, True])
        stage.verify_stage('competing')

    def test_run_id_cannot_reach_existing_source(self):
        for name in ('../src', '/tmp/escape', 'src/file', '.hidden', '', 'x\\y', 'x:bad'):
            with self.subTest(name=name), self.assertRaises(stage.StagingError):
                self.run_source(name)
        self.spawn.assert_not_called()
        self.assertTrue(self.sentinel.is_file())

    def test_wrong_revision_and_corrupt_commit_are_rejected(self):
        content = self.pool[self.commit]
        self.pool[self.commit] = ('commit', content[1] + b'corruption')
        with self.assertRaisesRegex(stage.StagingError, 'hash mismatch'):
            self.run_source()
        self.assertFalse(stage.run_path('run1').exists())

    def test_missing_object_is_rejected_before_output_allocation(self):
        del self.pool[self.commit]
        with self.assertRaisesRegex(stage.StagingError, 'Missing object'):
            self.run_source()
        self.assertFalse((self.macos / '.migration-work').exists())

    def test_corrupt_tree_and_blob_are_detected(self):
        for kind in ('tree', 'blob'):
            oid = next(oid for oid, row in self.pool.items() if row[0] == kind)
            original = self.pool[oid]
            self.pool[oid] = (kind, original[1] + b'corrupt')
            with self.subTest(kind=kind), self.assertRaisesRegex(stage.StagingError, 'hash mismatch'):
                self.run_source()
            self.pool[oid] = original
        self.assertFalse(stage.run_path('run1').exists())

    def test_object_and_total_size_limits(self):
        with mock.patch.object(stage, 'MAX_OBJECT_BYTES', 10):
            with self.assertRaisesRegex(stage.StagingError, 'size limit'):
                self.run_source()
        with mock.patch.object(stage, 'MAX_TOTAL_BYTES', 3):
            with self.assertRaisesRegex(stage.StagingError, 'total size'):
                self.run_source()
        self.assertFalse(stage.run_path('run1').exists())

    def test_tree_entry_and_depth_limits(self):
        with mock.patch.object(stage, 'MAX_ENTRIES', 1):
            with self.assertRaisesRegex(stage.StagingError, 'entry limit'):
                self.run_source()
        with mock.patch.object(stage, 'MAX_DEPTH', 0):
            with self.assertRaisesRegex(stage.StagingError, 'depth limit'):
                self.run_source()

    def test_unsafe_names_duplicate_and_case_unicode_collisions(self):
        blob = self.blob(b'x')
        for names in (['..'], ['a/b'], ['.git'], ['x\\y'], ['x:ads'], ['bad\nname'],
                      ['trailing.'], ['Foo', 'foo'], ['caf\u00e9', 'cafe\u0301'], ['same', 'same']):
            self.select_tree(self.tree([('100644', name, blob) for name in names]))
            with self.subTest(names=names), self.assertRaises(stage.StagingError):
                self.run_source()
        self.assertFalse(stage.run_path('run1').exists())

    def test_symlinks_and_gitlinks_are_refused_before_output(self):
        for mode in ('120000', '160000'):
            self.select_tree(self.tree([(mode, 'unsupported', self.blob(b'target'))]))
            with self.subTest(mode=mode), self.assertRaisesRegex(stage.StagingError, 'Unsupported Git mode'):
                self.run_source()
        self.assertFalse((self.macos / '.migration-work').exists())

    def test_symlinked_staging_parent_cannot_escape(self):
        outside = self.root / 'outside'
        outside.mkdir(mode=0o700)
        (self.macos / '.migration-work').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(stage.StagingError):
            self.run_source()
        self.spawn.assert_not_called()
        self.assertEqual(list(outside.iterdir()), [])

    def test_foreign_owned_directory_is_refused_without_chown(self):
        with mock.patch.object(stage.os, 'getuid', return_value=987654):
            with self.assertRaisesRegex(stage.StagingError, 'Untrusted'):
                self.run_source()
        self.spawn.assert_not_called()

    def test_missing_git_and_wrong_object_type_are_refused(self):
        with mock.patch.object(stage.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(stage.StagingError, 'Git is required'):
                self.run_source()
        self.pool[self.commit] = ('blob', self.pool[self.commit][1])
        with self.assertRaisesRegex(stage.StagingError, 'unexpected Git object type'):
            self.run_source()
        self.assertFalse(stage.run_path('run1').exists())

    def test_malformed_tree_is_refused_before_output(self):
        self.select_tree(self.add('tree', b'100644 bad-name-without-null'))
        with self.assertRaisesRegex(stage.StagingError, 'Truncated Git tree'):
            self.run_source()
        self.assertFalse(stage.run_path('run1').exists())

    def test_source_repository_alias_is_rejected(self):
        alias = self.root / 'repo-link'
        alias.symlink_to(self.repository, target_is_directory=True)
        with self.assertRaises(stage.StagingError):
            stage.stage_source(alias, 'run1')
        self.spawn.assert_not_called()

    def test_writable_or_nonprivate_staging_directory_is_refused(self):
        root = self.macos / '.migration-work'
        root.mkdir(mode=0o755)
        with self.assertRaisesRegex(stage.StagingError, 'mode 0700'):
            self.run_source()
        root.chmod(0o777)
        with self.assertRaisesRegex(stage.StagingError, 'Writable non-sticky'):
            self.run_source()

    def test_failure_retains_partial_output_without_completion(self):
        original = stage.exclusive
        def fail(path, data, mode=0o600):
            if 'candidate-source' in path.parts:
                raise OSError('injected write failure')
            return original(path, data, mode)
        with mock.patch.object(stage, 'exclusive', side_effect=fail):
            with self.assertRaisesRegex(OSError, 'injected'):
                self.run_source()
        run = stage.run_path('run1')
        self.assertTrue((run / 'FAILED.json').is_file())
        self.assertFalse((run / 'COMPLETE.json').exists())
        with self.assertRaises(stage.StagingError):
            stage.verify_stage('run1')
        with self.assertRaises(stage.StagingError):
            self.run_source()

    def test_candidate_edit_cannot_change_pristine_and_is_detected(self):
        self.run_source()
        run = stage.run_path('run1')
        (run / 'candidate-source/VERSION').write_bytes(b'bad')
        self.assertEqual((run / 'pristine-source/VERSION').read_bytes(), b'2.6\n')
        with self.assertRaisesRegex(stage.StagingError, 'integrity mismatch'):
            stage.verify_stage('run1')

    def test_pristine_tamper_addition_and_mode_change_are_detected(self):
        for index, mutation in enumerate(('pristine', 'extra', 'mode')):
            name = 'tamper' + str(index)
            self.run_source(name)
            root = stage.run_path(name) / 'pristine-source'
            if mutation == 'pristine':
                (root / 'VERSION').write_bytes(b'bad')
            elif mutation == 'extra':
                (root / 'unexpected.txt').write_bytes(b'extra')
            else:
                (root / 'VERSION').chmod(0o600)
            with self.subTest(mutation=mutation), self.assertRaises(stage.StagingError):
                stage.verify_stage(name)

    def test_staged_symlink_and_hardlink_are_detected(self):
        for name in ('symlink', 'hardlink'):
            self.run_source(name)
            root = stage.run_path(name)
            file = root / 'candidate-source/VERSION'
            file.unlink()
            if name == 'symlink':
                file.symlink_to(root / 'pristine-source/VERSION')
            else:
                os.link(root / 'pristine-source/VERSION', file)
            with self.subTest(name=name), self.assertRaises((OSError, stage.StagingError)):
                stage.verify_stage(name)

    def test_manifest_omission_cannot_be_hidden_by_rehashing_completion(self):
        self.run_source()
        run = stage.run_path('run1')
        manifest = json.loads((run / 'manifest.json').read_text())
        manifest['entries'] = [r for r in manifest['entries'] if r['path'] != 'VERSION']
        (run / 'manifest.json').write_bytes(stage.encoded(manifest))
        for name in ('pristine-source', 'candidate-source'):
            (run / name / 'VERSION').unlink()
        with self.assertRaisesRegex(stage.StagingError, 'reconstruct'):
            stage.verify_stage('run1')

    def test_altered_commit_binding_and_completion_are_rejected(self):
        self.run_source()
        run = stage.run_path('run1')
        manifest = json.loads((run / 'manifest.json').read_text())
        original = stage.encoded(manifest)
        manifest['commit_hex'] += '00'
        (run / 'manifest.json').write_bytes(stage.encoded(manifest))
        with self.assertRaisesRegex(stage.StagingError, 'pinned revision'):
            stage.verify_stage('run1')
        (run / 'manifest.json').write_bytes(original)
        (run / 'COMPLETE.json').write_bytes(b'{}')
        with self.assertRaisesRegex(stage.StagingError, 'Completion record'):
            stage.verify_stage('run1')

    def test_malformed_record_types_duplicates_and_constants_are_refused(self):
        self.run_source()
        record = stage.run_path('run1') / 'manifest.json'
        for data in (b'[]', b'{"schema_version":1,"schema_version":1}', b'{"x":NaN}'):
            record.write_bytes(data)
            with self.subTest(data=data), self.assertRaises(stage.StagingError):
                stage.verify_stage('run1')

    def test_git_command_cannot_fetch_checkout_or_run_source(self):
        self.run_source()
        command = self.spawn.call_args.args[0]
        self.assertEqual(command[-2:], ['cat-file', '--batch'])
        environment = self.spawn.call_args.kwargs['env']
        self.assertEqual(environment['GIT_NO_LAZY_FETCH'], '1')
        self.assertEqual(environment['GIT_NO_REPLACE_OBJECTS'], '1')
        self.assertNotIn('PYTHONPATH', environment)
        self.assertNotIn('GIT_CONFIG_COUNT', environment)

    def test_cli_reports_refusal_and_success_without_importing_source(self):
        with mock.patch('sys.stdout', new_callable=io.StringIO) as output:
            self.assertEqual(stage.main(['--run-id', 'run1', '--source-repository', str(self.repository)]), 0)
            self.assertEqual(json.loads(output.getvalue())['status'], 'VERIFIED_SOURCE_ONLY')
        with mock.patch('sys.stdout', new_callable=io.StringIO) as output:
            self.assertEqual(stage.main(['--run-id', 'run1', '--source-repository', str(self.repository)]), 1)
            self.assertEqual(json.loads(output.getvalue())['status'], 'REFUSED')
        with mock.patch('sys.stdout', new_callable=io.StringIO):
            self.assertEqual(stage.main(['--run-id', 'run1', '--verify']), 0)


if __name__ == '__main__':
    unittest.main()
