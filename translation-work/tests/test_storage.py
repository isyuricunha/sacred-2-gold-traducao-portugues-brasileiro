import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from native import PATHS, RES, write_res
from toolkit import Project, STATE, TRANSLATIONS, blob


class StorageSafety(unittest.TestCase):
    def test_five_hundred_updates_no_full_tree_copies(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            data = {x: b'' for x in PATHS}
            data[RES] = write_res([], [(i, f'Text {i}') for i in range(120)])
            p = Project(root)
            p.sync(data, initial=True)
            manifest, _, batches = p.load()
            rows = [r for batch in batches.values() for r in batch]
            p.path(TRANSLATIONS + '/' + manifest['batches'][0]).unlink()
            manifest['batches'] = [f'batch-{i+1:04d}.jsonl' for i in range(len(rows))]
            for name, row in zip(manifest['batches'], rows):
                p.path(TRANSLATIONS + '/' + name).write_bytes(
                    (json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n').encode())
            p.path(TRANSLATIONS + '/manifest.json').write_bytes(blob(manifest))
            self.assertGreaterEqual(len(manifest['batches']), 100)
            untouched = p.path(TRANSLATIONS + '/' + manifest['batches'][1])
            unchanged = (untouched.read_bytes(), untouched.stat().st_mtime_ns)
            row = rows[0]
            for i in range(500):
                p.apply({'generation': manifest['generation'], 'entries': [{
                    'id': row['id'], 'source_fingerprint': row['source_fingerprint'],
                    'PTBR': 'Texto A' if i % 2 else 'Texto B'}]}, replace=True)
            self.assertEqual((untouched.read_bytes(), untouched.stat().st_mtime_ns), unchanged)
            self.assertLessEqual(len(list(p.path(STATE + '/transactions').iterdir())), 10)
            self.assertEqual(p.gc(dry_run=True)['removed'], 0)

    def test_gc_dryrun_prunes_only_completed_and_protects_journal(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            data = {x: b'' for x in PATHS}
            data[RES] = write_res([], [(1, 'Text')])
            p = Project(root)
            p.sync(data, initial=True)
            manifest, _, batches = p.load()
            row = next(iter(next(iter(batches.values()))))
            with mock.patch.object(p, 'gc', return_value={}):
                for i in range(14):
                    p.apply({'generation': manifest['generation'], 'entries': [{
                        'id': row['id'], 'source_fingerprint': row['source_fingerprint'],
                        'PTBR': 'Texto A' if i % 2 else 'Texto B'}]}, replace=True)
            before = {x.name for x in p.path(STATE + '/transactions').iterdir()}
            self.assertGreater(p.gc(dry_run=True)['removed'], 0)
            self.assertEqual(before, {x.name for x in p.path(STATE + '/transactions').iterdir()})
            self.assertGreater(p.gc()['removed'], 0)
            self.assertLessEqual(len(list(p.path(STATE + '/transactions').iterdir())), 10)
            expected = p.state_inventory()
            with self.assertRaises(RuntimeError):
                p.transaction({TRANSLATIONS + '/batch-0001.jsonl': b'bad'},
                              [TRANSLATIONS + '/batch-0001.jsonl'], expected, fail_after=0)
            before = {x.name for x in p.path(STATE + '/transactions').iterdir()}
            with self.assertRaises(ValueError):
                p.gc()
            self.assertEqual(before, {x.name for x in p.path(STATE + '/transactions').iterdir()})
            p.recover()
            self.assertEqual(expected, p.state_inventory())


if __name__ == '__main__':
    unittest.main()
