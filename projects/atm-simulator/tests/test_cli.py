"""End-to-end checks against the actual terminal executable."""

from pathlib import Path
import subprocess
import unittest


BINARY = Path(__file__).resolve().parents[1] / "build" / "atm"
DEMO_PIN = "2486"  # Public fixture for the original classroom demo.


def invoke(*lines, args=()):
    return subprocess.run(
        [str(BINARY), *args],
        input="".join(line + "\n" for line in lines),
        capture_output=True,
        text=True,
        timeout=3,
        check=False,
    )


class TerminalTests(unittest.TestCase):
    def session(self, *commands):
        result = invoke(DEMO_PIN, *commands)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_starting_balance(self):
        self.assertIn("Balance: 10000", self.session("1"))

    def test_successful_withdrawal(self):
        output = self.session("2", "75")
        self.assertIn("Withdrawal amount: 75", output)
        self.assertIn("Remaining balance: 9925", output)

    def test_refuses_overdraft(self):
        self.assertIn("insufficient balance", self.session("2", "10001").lower())
