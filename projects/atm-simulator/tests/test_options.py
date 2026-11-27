import unittest

from terminal_driver import DEMO_PIN, invoke


class StartupOptionsTests(unittest.TestCase):
    def test_help_does_not_start_a_session(self):
        for flag in ("--help", "-h"):
            result = invoke(args=(flag,))
            self.assertEqual(result.returncode, 0)
            self.assertIn("--opening-balance AMOUNT", result.stdout)
            self.assertNotIn("Choose a four-digit demo PIN", result.stdout)
            self.assertEqual(result.stderr, "")

    def test_custom_opening_balance(self):
        result = invoke(DEMO_PIN, DEMO_PIN, "1", args=("--opening-balance", "12.3"))
        self.assertEqual(result.returncode, 0)
        self.assertIn("Balance: 12.30", result.stdout)

    def test_invalid_options_fail_before_account_setup(self):
        for args in [
            ("--unknown",), ("12",), ("--opening-balance",),
            ("--opening-balance", "-1"), ("--opening-balance", "0.001"),
            ("--opening-balance", "184467440737095516.16"),
            ("--opening-balance", "0", "--opening-balance", "2"),
        ]:
            with self.subTest(args=args):
                result = invoke(args=args)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Usage:", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_opening_balance_accepts_both_endpoints(self):
        for amount in ("0.00", "184467440737095516.15"):
            with self.subTest(amount=amount):
                result = invoke(DEMO_PIN, DEMO_PIN, "1", "0", args=("--opening-balance", amount))
                self.assertEqual(result.returncode, 0)
                self.assertIn(f"Balance: {amount}\n", result.stdout)
