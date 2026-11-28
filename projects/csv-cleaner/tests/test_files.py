from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from test_cli import run


class OutputTests(unittest.TestCase):
    def test_new_file_is_published_only_after_validation(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "out.csv"
            self.assertEqual(run("clean", "-o", str(path), text="a,b\n1\n")[0], 1)
            self.assertEqual(list(Path(d).iterdir()), [])
            self.assertEqual(run("clean", "-o", str(path), text="a\n1")[0], 0)
            self.assertEqual(path.read_bytes(), b"a\r\n1\r\n")
            self.assertEqual(run("clean", "-o", str(path), text="x\n2")[0], 2)
            self.assertEqual(path.read_bytes(), b"a\r\n1\r\n")
