import io
import unittest

from csvclean.cli import main


def run(*args, text=""):
    out, err = io.StringIO(newline=""), io.StringIO()
    status = main(args, stdin=io.StringIO(text, newline=""), stdout=out, stderr=err)
    return status, out.getvalue(), err.getvalue()


class ValidateTests(unittest.TestCase):
    def test_valid_stdin(self):
        self.assertEqual(run("validate", text="a,b\n1,2\n"), (0, "OK: 1 data rows, 2 columns\n", ""))

    def test_invalid_input_has_data_exit_status(self):
        rc, out, err = run("validate", text="a,b\n1\n")
        self.assertEqual((rc, out), (1, ""))
        self.assertIn("line 2", err)

    def test_file_argument_and_missing_file_diagnostic(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            rc, _, err = run("validate", str(path))
            self.assertEqual(rc, 2)
            self.assertIn("input error", err)
            path.write_bytes(b"a,b\r\n1,2\r\n")
            self.assertEqual(run("validate", str(path))[0], 0)
