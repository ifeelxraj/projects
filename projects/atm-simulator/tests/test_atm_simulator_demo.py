"""Keep the replayable session and its documented results in sync."""

from pathlib import Path
import unittest

from atm_simulator_test_terminal_driver import invoke


class ExampleTests(unittest.TestCase):
    def test_mini_statement_replay(self):
        example = Path(__file__).resolve().parents[1] / "examples" / "atm-simulator-mini-statement.in"
        result = invoke(
            *example.read_text().splitlines(),
            args=("--opening-balance", "25.00", "--cash-limit", "7.00"),
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertIn("Withdrawal -5.20 | balance 22.55\nDeposit +2.75 | balance 27.75", result.stdout)
        self.assertIn("Balance: 22.55\nCash allowance left: 1.80", result.stdout)
        self.assertNotIn("Invalid choice.", result.stdout)
