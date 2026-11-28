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
