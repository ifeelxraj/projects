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
