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
