import unittest

from test_csv_cleaner_commands import run


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

    def test_calendar_dates_must_exist_and_have_canonical_spelling(self):
        for value, code in [("2024-02-29", 0), ("2023-02-29", 1), ("20240102", 1), ("2024-W01-1", 1)]:
            with self.subTest(value=value):
                self.assertEqual(run("validate", "--date", "d", text=f"d\n{value}\n")[0], code)

    def test_decimal_rule_accepts_arbitrary_precision_but_not_special_values(self):
        for value, code in [("-12.00000000000000001", 0), ("5", 0), ("1e2", 1), ("NaN", 1), ("inf", 1), ("1.", 1)]:
            self.assertEqual(run("validate", "--decimal", "value", text=f"value\n{value}")[0], code)
