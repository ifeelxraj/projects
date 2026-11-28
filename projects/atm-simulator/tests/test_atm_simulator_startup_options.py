import unittest

from atm_simulator_test_terminal_driver import DEMO_PIN, invoke


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

    def test_allowance_survives_deposit_and_reauthentication(self):
        result = invoke(
            DEMO_PIN, DEMO_PIN, "2", "0.03", "4", "1", "6", DEMO_PIN,
            "2", "0.03", "2", "0.02", "1", "5", "0",
            args=("--cash-limit", "0.05", "--opening-balance", "1"),
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("exceeds the remaining cash allowance", result.stdout)
        self.assertIn("Cash allowance left: 0.00", result.stdout)
        self.assertIn("Balance: 1.95", result.stdout)
        self.assertEqual(result.stdout.count("Withdrawal -"), 2)

    def test_zero_allowance_blocks_only_withdrawals(self):
        result = invoke(DEMO_PIN, DEMO_PIN, "4", "2", "2", "0.01", "1", args=("--cash-limit", "0"))
        self.assertIn("Cash allowance left: 0.00", result.stdout)
        self.assertIn("Balance: 10002.00", result.stdout)
