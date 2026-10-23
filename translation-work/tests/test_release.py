import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import release


class ReleaseFlow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.work = self.root / 'translation-work'
        (self.work / 'translations').mkdir(parents=True)
        (self.root / 'PTBR/locale/en_UK').mkdir(parents=True)
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.email', 'tests@example.invalid')
        self.git('config', 'user.name', 'Tests')
        self.row = {'id': 'locale/en_UK/global.res#1', 'EN': 'Hello', 'PTBR': 'Olá'}
        self.update_files('first', 'Olá')
        self.commit()
        self.patches = [mock.patch.object(release, 'ROOT', self.root),
                        mock.patch.object(release, 'WORK', self.work)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout

    def commit(self):
        self.git('add', '-A')
        self.git('commit', '-qm', 'Updated translation')

    def update_files(self, native, ptbr):
        (self.root / 'PTBR/locale/en_UK/global.res').write_bytes(native.encode())
        self.row['PTBR'] = ptbr
        (self.work / 'translations/batch-0001.jsonl').write_text(
            json.dumps(self.row, ensure_ascii=False) + '\n', encoding='utf-8')
        (self.work / 'build-manifest.json').write_text(
            json.dumps({'pending': 0, 'completed': 1, 'records': 1}), encoding='utf-8')
        with zipfile.ZipFile(self.root / 'PTBR.zip', 'w') as z:
            z.write(self.root / 'PTBR/locale/en_UK/global.res',
                    'locale/en_UK/global.res')

    def test_first_release_increment_changelog_and_idempotence(self):
        initial = release.plan([], 'isyuricunha/sacred-2-gold-traducao-portugues-brasileiro')
        self.assertEqual(initial['tag'], 'v1.0.0')
        self.assertTrue(initial['publish'])
        self.assertIn('Primeira versão', initial['notes'])
        self.git('tag', 'v1.0.0')
        published = [{'tagName': 'v1.0.0', 'isDraft': False, 'isPrerelease': False}]
        again = release.plan(published, 'isyuricunha/sacred-2-gold-traducao-portugues-brasileiro')
        self.assertFalse(again['publish'])
        self.update_files('second', 'Bom dia')
        self.commit()
        next_release = release.plan(published, 'isyuricunha/sacred-2-gold-traducao-portugues-brasileiro')
        self.assertEqual(next_release['tag'], 'v1.0.1')
        self.assertIn('**1** textos revisados/alterados.', next_release['notes'])
        self.assertIn('global.res', next_release['notes'])
        self.git('tag', 'v1.0.1')
        versioned = published + [{'tagName': 'v1.0.1', 'isDraft': False, 'isPrerelease': False}]
        self.assertFalse(release.plan(versioned, 'org/repo')['publish'])

    def test_unpublished_tag_collision_fails_closed(self):
        self.git('tag', 'v1.0.0')
        self.update_files('new-native', 'Texto novo')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'exists at a different commit'):
            release.plan([], 'org/repo')

    def test_missing_native_output_rejected(self):
        (self.root / 'PTBR/locale/en_UK/global.res').unlink()
        self.commit()
        with self.assertRaises(ValueError):
            release.plan([], 'org/repo')


if __name__ == '__main__':
    unittest.main()
