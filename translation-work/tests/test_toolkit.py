import argparse
import copy
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import subprocess
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from native import PATHS, RES, read_res, write_res, records, rebuild, validate_translation
from toolkit import Project, TRANSLATIONS, SNAPSHOT, REPORTS, BUILD, STATE, blob, read_json, source_inventory, fingerprint, inventory


class Workflow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='sacred2 tests ')
        self.root = Path(self.tmp.name) / 'repository'
        self.root.mkdir()
        (self.root / 'translation-work').mkdir()
        for name in ('toolkit.py', 'native.py'):
            shutil.copy(Path(__file__).resolve().parents[1] / name, self.root / 'translation-work' / name)
        self.p = Project(self.root)
        self.sources = {n: b'' for n in PATHS}
        self.sources[RES] = write_res([1, 2, 3], [(10, 'Hello %1<br>World'), (20, 'Name'), (30, 'Name')])
        self.sources['locale/en_UK/Itemnames.csv'] = b'NGCLF_SWORD;Sword,1;Blade,1\r\n'
        self.sources['locale/en_UK/AppendBonus.csv'] = b'hasGender=false;\r\nBON;of Fire;of Ice\r\n'
        self.p.sync(self.sources, initial=True)

    def tearDown(self):
        self.tmp.cleanup()

    def payload(self, items=None):
        m, _, batches = self.p.load()
        rows = [r for group in batches.values() for r in group]
        return {'generation': m['generation'], 'entries': [
            {k: r[k] for k in ('id', 'source_fingerprint')} | {'PTBR': r['EN']}
            for r in (rows if items is None else items)]}

    def complete(self):
        self.p.apply(self.payload())

    def rows(self):
        return {r['id']: r for b in self.p.load()[2].values() for r in b}

    def test_native_roundtrip_and_unicode(self):
        pairs = [(1, 'Ação, bênção, Órgão — 😀'), (2, ''), (3, 'ç' * 30)]
        b = write_res([8, 9], pairs)
        self.assertEqual(read_res(b), ([8, 9], pairs))
        for p, data in self.sources.items():
            self.assertEqual(rebuild(p, data, {r['id']: r['EN'] for r in records(p, data)}), data)
        self.assertEqual(read_res(write_res([], [])), ([], []))

    def test_single_character(self):
        self.assertEqual(read_res(write_res([], [(1, 'ç' * 80)]))[1], [(1, 'ç' * 80)])

    def test_bad_native(self):
        for data in (b'', b'bad format' * 4, self.sources[RES][:45]):
            with self.assertRaises((ValueError, struct.error)):
                read_res(data)
        with self.assertRaises(ValueError):
            write_res([], [(1, 'a'), (1, 'b')])
        with self.assertRaises(ValueError):
            records('locale/en_UK/Itemnames.csv', b'KEY;A,1\nKEY;B,1\n')

    def test_extract_batches_500(self):
        root = self.root / 'other'
        root.mkdir()
        p = Project(root)
        data = dict(self.sources, **{RES: write_res([], [(i, 'text') for i in range(1001)])})
        p.sync(data, initial=True)
        self.assertEqual([len(b) for b in p.load()[2].values()], [500, 500, 5])
        with self.assertRaises(ValueError):
            p.sync(data, initial=True)

    def test_progress_no_output_and_incomplete_gate(self):
        old = self.p.state_inventory()
        self.p.apply(self.payload(list(self.rows().values())[:1]))
        self.assertEqual(self.p.state_inventory()['PTBR'], old['PTBR'])
        self.p.load()
        with self.assertRaises(ValueError):
            self.p.build()
        self.assertFalse((self.root / 'PTBR').exists())

    def test_partial_apply_and_retry(self):
        payload = self.payload()
        payload['entries'][0]['PTBR'] = 'broken tags'
        result = self.p.apply(payload)
        self.assertEqual(len(result['rejected']), 1)
        self.assertEqual(len(result['accepted']), 6)
        self.assertEqual(self.p.apply(payload)['accepted'], [])

    def test_wrong_generation_unknown_duplicate_and_overwrite(self):
        for kind in ('generation', 'unknown', 'duplicate', 'fingerprint', 'immutable'):
            payload = self.payload()
            if kind == 'generation': payload['generation'] = 'bad'
            if kind == 'unknown': payload['entries'][0]['id'] = 'bad'
            if kind == 'duplicate': payload['entries'].append(payload['entries'][0])
            if kind == 'fingerprint': payload['entries'][0]['source_fingerprint'] = 'bad'
            if kind == 'immutable': payload['entries'][0]['EN'] = 'bad'
            before = self.p.state_inventory()
            with self.assertRaises(ValueError): self.p.apply(payload)
            self.assertEqual(before, self.p.state_inventory())
        self.complete()
        payload = self.payload()
        payload['entries'][1]['PTBR'] = 'Nome'
        self.assertTrue(self.p.apply(payload)['rejected'])
        self.assertTrue(self.p.apply(payload, replace=True)['accepted'])

    def test_incremental_change_add_delete_reorder(self):
        self.complete()
        sources = dict(self.sources)
        sources[RES] = write_res([1, 2, 3], [(30, 'Name'), (10, 'Changed %1<br>World'), (40, 'New')])
        result = self.p.sync(sources)
        self.assertEqual(result['counts']['modified'], 1)
        self.assertEqual(result['counts']['removed'], 1)
        self.assertEqual(result['counts']['added'], 1)
        rows = self.rows()
        self.assertEqual(rows[RES + '#30']['PTBR'], 'Name')
        self.assertEqual(rows[RES + '#10']['PTBR'], '')
        self.assertEqual(rows[RES + '#10']['history'][0]['PTBR'], 'Hello %1<br>World')
        self.assertEqual(read_json(self.root / REPORTS / 'sync-latest.json')['changes'][0]['kind'], 'moved')

    def test_direct_overwrite_en_and_noop(self):
        self.complete()
        before = self.p.state_inventory()
        self.assertEqual(self.p.sync()['status'], 'unchanged')
        self.assertEqual(before, self.p.state_inventory())
        (self.root / 'EN' / RES).write_bytes(write_res([1, 2, 3], [(10, 'Changed %1<br>World'), (20, 'Name'), (30, 'Name')]))
        self.assertTrue(self.p.status()['en_changed'])
        result = self.p.sync()
        self.assertEqual(result['counts']['modified'], 1)
        self.assertEqual(result['counts']['preserved_translations'], 6)

    def test_missing_source_catalog_and_corrupt_batches(self):
        file = self.root / SNAPSHOT / RES
        data = file.read_bytes()
        file.unlink()
        with self.assertRaises(ValueError): self.p.sync(self.sources)
        file.write_bytes(data)
        batch = self.root / TRANSLATIONS / 'batch-0001.jsonl'
        batch.write_text('{}\n', encoding='utf8')
        with self.assertRaises((ValueError, KeyError)): self.p.load()

    def test_batch_assignment_preservation(self):
        self.complete()
        _, _, groups = self.p.load()
        ids = [r['id'] for r in groups['batch-0001.jsonl']]
        sources = dict(self.sources)
        sources[RES] = write_res([1, 2, 3], [(30, 'Name'), (20, 'Name'), (10, 'Hello %1<br>World'), (40, 'Added')])
        self.p.sync(sources)
        _, _, groups = self.p.load()
        self.assertEqual([r['id'] for r in groups['batch-0001.jsonl']][:7], ids)

    def test_dry_run_missing_and_extra_files(self):
        before = self.p.state_inventory()
        changed = dict(self.sources)
        changed[RES] = write_res([], [(1, 'new')])
        self.p.sync(changed, dry_run=True)
        self.assertEqual(before, self.p.state_inventory())
        for bad in ({RES: changed[RES]}, dict(changed, **{'extra.res': b'a'})):
            with self.assertRaises(ValueError): self.p.sync(bad)
        self.assertEqual(before, self.p.state_inventory())

    def test_safe_paths_and_symlinks(self):
        for path in ('../escape', 'EN/../../escape', '/absolute', 'a\\b', 'C:/bad'):
            with self.assertRaises(ValueError): self.p.path(path)
        external = self.root.parent / 'external'
        external.mkdir()
        try:
            (self.root / 'linked').symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest('OS does not allow symlink creation')
        with self.assertRaises(ValueError): self.p.path('linked/file')

    def test_lock(self):
        with self.p.lock():
            with self.assertRaises(ValueError):
                with self.p.lock(): pass

    def test_conflict_and_crash_recovery(self):
        before = self.p.state_inventory()
        files = {'EN/a': b'new', SNAPSHOT + '/a': b'new'}
        with self.assertRaises(RuntimeError):
            self.p.transaction(files, ['EN', SNAPSHOT], before, fail_after=0)
        with self.assertRaises(ValueError): self.p.load()
        self.p.recover()
        self.assertEqual(before, self.p.state_inventory())
        before = self.p.state_inventory()
        (self.root / 'EN' / RES).write_bytes(b'concurrent edit')
        with self.assertRaises(ValueError): self.p.transaction(files, ['EN'], before)

    def test_crash_build_pair_and_preserve_old_output(self):
        self.complete()
        self.p.build()
        before = self.p.state_inventory()
        files = {'PTBR/a': b'new', BUILD: b'new'}
        with self.assertRaises(RuntimeError): self.p.transaction(files, ['PTBR', BUILD], before, fail_after=0)
        self.p.recover()
        self.assertEqual(before, self.p.state_inventory())
        self.p.verify_output()

    def test_complete_build_verify_zip_and_staleness(self):
        self.complete()
        self.p.build()
        self.p.verify_output()
        self.assertEqual(self.p.build()['status'], 'unchanged')
        self.p.package()
        with zipfile.ZipFile(self.root / 'PTBR.zip') as archive:
            self.assertEqual(set(archive.namelist()), set(PATHS))
            self.assertFalse(any(n.startswith('PTBR/') for n in archive.namelist()))
        self.p.path('PTBR/extra.txt').write_text('extra')
        with self.assertRaises(ValueError): self.p.verify_output()
        self.p.path('PTBR/extra.txt').unlink()
        native = self.p.path('PTBR/' + RES)
        good = native.read_bytes()
        native.write_bytes(b'bad')
        with self.assertRaises(ValueError): self.p.verify_output()
        native.write_bytes(good)
        native.unlink()
        with self.assertRaises(ValueError): self.p.verify_output()
        native.write_bytes(good)
        manifest = self.p.path(BUILD)
        receipt = manifest.read_bytes()
        manifest.write_bytes(blob({'complete': True}))
        with self.assertRaises(ValueError): self.p.verify_output()
        manifest.write_bytes(receipt)
        self.p.verify_output()
        payload = self.payload()
        payload['entries'][1]['PTBR'] = 'Nome'
        self.p.apply(payload, replace=True)
        with self.assertRaises(ValueError): self.p.verify_output()
        self.assertEqual(native.read_bytes(), good)

    def test_native_build_failure_keeps_ptbr(self):
        self.complete()
        self.p.build()
        before = self.p.state_inventory()
        with mock.patch('toolkit.rebuild', side_effect=ValueError('native failure')):
            with self.assertRaises(ValueError): self.p.build()
        self.assertEqual(before, self.p.state_inventory())

    def test_protected_syntax_and_csv(self):
        row = next(iter(self.rows().values()))
        for bad in ('Hello World', 'Hello %2<br>World', 'Hello %1<br><br>World'):
            with self.assertRaises(ValueError): validate_translation(dict(row, PTBR=bad))
        validate_translation(dict(row, PTBR='Olá %1<br>Mundo'))
        csv = next(r for r in self.rows().values() if r['source_file'].endswith('Itemnames.csv'))
        for bad in ('bad;value', '😀', 'new\nline'):
            with self.assertRaises((ValueError, UnicodeError)): validate_translation(dict(csv, PTBR=bad))
        validate_translation(dict(csv, PTBR='Espadão'))

    def test_game_discovery_fallback_trust_and_readonly(self):
        args = argparse.Namespace(source_file=None, source_root=None, game_root=None,
                                  command='update-sources', approve_source=None, dry_run=True)
        with mock.patch.dict('os.environ', {'ProgramFiles(x86)': str(self.root / 'no steam')}):
            with self.assertRaisesRegex(ValueError, '--game-root'): self.p.candidate(args)
        game = self.root.parent / 'Sacred 2 game with spaces'
        for name, data in self.sources.items():
            p = game / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        args.game_root = str(game)
        with self.assertRaisesRegex(ValueError, 'Not Sacred 2'): self.p.candidate(args)
        (game / 'system').mkdir()
        (game / 'system/sacred2.exe').write_bytes(b'fixture')
        digest = fingerprint(source_inventory(self.sources))
        self.p.path('translation-work/source-policy.json').write_bytes(blob({'trusted': [digest], 'rejected': []}))
        before = inventory(game)
        self.assertEqual(self.p.candidate(args), self.sources)
        self.assertEqual(before, inventory(game))
        (game / RES).write_bytes(write_res([], [(1, 'Unknown edition')]))
        with self.assertRaisesRegex(ValueError, 'Unrecognized'): self.p.candidate(args)
        self.p.path('translation-work/source-policy.json').write_bytes(blob({'trusted': [], 'rejected': [fingerprint(source_inventory({n: (game/n).read_bytes() for n in PATHS}))]}))
        with self.assertRaisesRegex(ValueError, 'Known translated'): self.p.candidate(args)

    def test_empty_duplicate_csv_row_preserved(self):
        data = b'KEY;Fire;Ice\r\nKEY;;\r\n'
        path = 'locale/en_UK/AppendBonus.csv'
        rows = records(path, data)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rebuild(path, data, {r['id']: r['EN'] for r in rows}), data)

    def test_source_change_stales_output_without_replacing_it(self):
        self.complete()
        self.p.build()
        before = inventory(self.root / 'PTBR')
        sources = dict(self.sources)
        sources[RES] = write_res([1, 2, 3], [(10, 'Changed %1<br>World'), (20, 'Name'), (30, 'Name')])
        self.p.sync(sources)
        with self.assertRaises(ValueError): self.p.verify_output()
        with self.assertRaises(ValueError): self.p.build()
        self.assertEqual(before, inventory(self.root / 'PTBR'))

    def test_readonly_verifier_does_not_native_rebuild(self):
        self.complete()
        self.p.build()
        before = self.p.state_inventory()
        with mock.patch('toolkit.rebuild', side_effect=AssertionError('CI must not rebuild')):
            self.p.verify_output()
            self.p.package()
        self.assertEqual(before, self.p.state_inventory())

    def test_cli_from_other_working_directory(self):
        result = subprocess.run([sys.executable, '-B', str(self.root / 'translation-work/toolkit.py'),
                                 'status', '--json'], cwd=self.root.parent, capture_output=True, encoding='utf8')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['pending'], 7)

    def test_publication_trigger_contract(self):
        root = Path(__file__).resolve().parents[2]
        workflow = (root / '.github/workflows/release.yml').read_text(encoding='utf8')
        self.assertIn('branches: [main]', workflow)
        self.assertIn("- 'PTBR/**'", workflow)
        paths = workflow.split('paths:', 1)[1].split('workflow_dispatch:', 1)[0]
        self.assertNotIn('translation-work', paths)
        self.assertNotIn('EN/', paths)
        self.assertIn('contents: write', workflow)
        self.assertIn('concurrency:', workflow)
        self.assertIn('release.py plan', workflow)
        self.assertIn('gh release create', workflow)
        self.assertIn('workflow_dispatch:', workflow)
        self.assertIn('verify-output', workflow)
        self.assertNotIn('toolkit.py build', workflow)
        self.assertIn('actions/upload-artifact@v7', workflow)


if __name__ == '__main__':
    unittest.main()
