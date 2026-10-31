import concurrent.futures
import importlib.util
import os
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('publisher', Path(__file__).resolve().parents[1] / 'preview-service/scripts/publish.py')
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


class Publishing(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.public = self.root / 'previews'
        self.public.mkdir()
        self.public.chmod(0o2750)
        self.source = self.root / 'design.html'
        self.source.write_text('<html>first</html>')
        self.config = {'preview_root': str(self.public), 'base_url': 'https://mini.example.ts.net:8443'}
        self.requests = []
        def verify(url, data):
            path = self.public / url.split(':8443/')[1]
            if path.is_dir():
                path /= 'index.html'
            self.assertEqual(path.read_bytes(), data)
            self.requests.append(url)
        self.verifier = patch.object(publisher, 'verify', side_effect=verify)
        self.verifier.start()
        self.addCleanup(self.verifier.stop)

    def test_revisions_keep_history_and_readable_url(self):
        first = publisher.publish(self.config, self.source, 'jarvis-connections', new=True)
        self.source.write_text('<html>second</html>')
        second = publisher.publish(self.config, self.source, 'jarvis-connections')
        task = self.public / 'jarvis-connections'
        self.assertEqual((task / 'v1.html').read_text(), '<html>first</html>')
        self.assertEqual((task / 'v2.html').read_bytes(), (task / 'index.html').read_bytes())
        self.assertEqual(first['url'], second['url'])
        self.assertEqual(second['revision'], 2)
        self.assertEqual(len(list(self.public.iterdir())), 1)
        self.assertEqual(len(self.requests), 4)

    def test_new_task_collision_does_not_publish(self):
        publisher.publish(self.config, self.source, 'design', new=True)
        with self.assertRaises(FileExistsError):
            publisher.publish(self.config, self.source, 'design', new=True)
        self.assertFalse((self.public / 'design/v2.html').exists())

    def test_restrictive_umask_keeps_service_read_access(self):
        previous = os.umask(0o077)
        try:
            publisher.publish(self.config, self.source, 'design', new=True)
        finally:
            os.umask(previous)
        task = self.public / 'design'
        self.assertEqual(task.stat().st_mode & 0o777, 0o750)
        if sys.platform.startswith('linux'):
            self.assertTrue(task.stat().st_mode & 0o2000)
        for name in ['v1.html', 'index.html']:
            self.assertEqual((task / name).stat().st_mode & 0o777, 0o640)
            self.assertEqual((task / name).stat().st_gid, self.public.stat().st_gid)

    def test_missing_task_needs_explicit_creation(self):
        with self.assertRaisesRegex(ValueError, '--new'):
            publisher.publish(self.config, self.source, 'design')

    def test_parallel_revisions_are_distinct(self):
        publisher.publish(self.config, self.source, 'design', new=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: publisher.publish(self.config, self.source, 'design'), range(12)))
        self.assertEqual(sorted(r['revision'] for r in results), list(range(2, 14)))
        self.assertEqual(len(list((self.public / 'design').glob('v*.html'))), 13)

    def test_verification_failure_keeps_previous_latest(self):
        publisher.publish(self.config, self.source, 'design', new=True)
        self.source.write_text('<html>second</html>')
        with patch.object(publisher, 'verify', side_effect=OSError('Tailscale unavailable')):
            with self.assertRaisesRegex(ValueError, 'latest was not updated'):
                publisher.publish(self.config, self.source, 'design')
        self.assertEqual((self.public / 'design/index.html').read_text(), '<html>first</html>')
        self.assertEqual((self.public / 'design/v2.html').read_text(), '<html>second</html>')

    def test_paths_and_links_are_rejected(self):
        for task in ['../escape', '/absolute', 'has space', 'Uppercase', 'foo/bar']:
            with self.subTest(task=task), self.assertRaises(ValueError):
                publisher.publish(self.config, self.source, task, new=True)
        link = self.root / 'link.html'
        link.symlink_to(self.source)
        with self.assertRaises(OSError):
            publisher.publish(self.config, link, 'design', new=True)
        (self.public / 'linked').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            publisher.publish(self.config, self.source, 'linked')
        self.assertFalse((self.root / 'v1.html').exists())

    def test_public_or_redirected_verification_is_rejected(self):
        for base in ['http://mini.example.ts.net', 'https://example.com', 'https://mini.example.ts.net/path']:
            with self.subTest(base=base), self.assertRaises(ValueError):
                publisher.publish(dict(self.config, base_url=base), self.source, 'design', new=True)
        with self.assertRaisesRegex(ValueError, 'redirected'):
            publisher.NoRedirect().redirect_request(None, None, None, None, None, 'https://example.com')


if __name__ == '__main__':
    unittest.main()
