from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from test_csv_cleaner_commands import run


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

    def test_replace_preserves_old_contents_on_late_validation_failure(self):
        with TemporaryDirectory() as d:
            dest = Path(d) / "out.csv"
            dest.write_bytes(b"keep")
            cmd = ("clean", "--replace", "-o", str(dest))
            self.assertEqual(run(*cmd, text="a,b\n1,2\n3")[0], 1)
            self.assertEqual(dest.read_bytes(), b"keep")
            self.assertEqual(run(*cmd, text="a\n1")[0], 0)
            self.assertEqual(dest.read_bytes(), b"a\r\n1\r\n")

    def test_replace_rejects_an_alias_of_the_input(self):
        import os
        with TemporaryDirectory() as d:
            source, dest = Path(d) / "source.csv", Path(d) / "alias.csv"
            source.write_bytes(b"a\noriginal\n")
            os.link(source, dest)
            rc, _, err = run("clean", str(source), "-o", str(dest), "--replace")
            self.assertEqual(rc, 2)
            self.assertIn("same file", err)
            self.assertEqual(dest.read_bytes(), source.read_bytes())

    def test_competing_creation_cannot_be_overwritten_at_publication(self):
        from csvclean.csv_cleaner_file_io import output_stream
        with TemporaryDirectory() as d:
            dest = Path(d) / "race.csv"
            with self.assertRaises(FileExistsError):
                with output_stream(dest, None) as pending:
                    pending.write("candidate")
                    dest.write_text("competitor", encoding="utf-8")
            self.assertEqual(dest.read_text(encoding="utf-8"), "competitor")
            self.assertEqual(list(Path(d).iterdir()), [dest])

    def test_writer_exception_does_not_leak_temporary_files(self):
        from csvclean.csv_cleaner_file_io import output_stream
        with TemporaryDirectory() as d:
            with self.assertRaisesRegex(RuntimeError, "interrupt"):
                with output_stream(Path(d) / "out.csv", None) as pending:
                    pending.write("partial")
                    raise RuntimeError("interrupt")
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_replace_cannot_destroy_the_rule_file(self):
        with TemporaryDirectory() as d:
            config = Path(d) / "rules.json"
            data = b'{"version":1,"columns":["a"]}'
            config.write_bytes(data)
            rc, _, err = run("clean", "--schema", str(config), "--replace", "-o", str(config), text="a\n1")
            self.assertEqual(rc, 2)
            self.assertIn("same file", err)
            self.assertEqual(config.read_bytes(), data)
