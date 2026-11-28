import unittest

from test_cli import run


class RuleTests(unittest.TestCase):
    def test_required_checks_raw_values_even_when_column_is_dropped(self):
        sample = "id,note\n ,ok\n"
        for cmd in [("validate",), ("clean", "--drop", "id", "--fill-empty", "fallback")]:
            rc, _, err = run(*cmd, "--require", "id", text=sample)
            self.assertEqual(rc, 1)
            self.assertIn("line 2: column 'id' must not be blank", err)
        self.assertEqual(run("validate", "--require", "typo", text=sample)[0], 2)

    def test_integer_check_is_textual_not_a_lossy_conversion(self):
        sample = 'n\n+001\n-2\n""\n' + "9" * 5000 + "\n"
        self.assertEqual(run("validate", "--integer", "n", text=sample)[0], 0)
        for value in ("3.0", "2e1", "１２", " 3"):
            self.assertEqual(run("validate", "--integer", "n", text=f"n\n{value}\n")[0], 1)
