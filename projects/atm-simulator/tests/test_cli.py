"""End-to-end checks against the actual terminal executable."""

from pathlib import Path
import subprocess
import unittest


BINARY = Path(__file__).resolve().parents[1] / "build" / "atm"
DEMO_PIN = "0042"  # Made-up for this in-memory test account.


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
        result = invoke(DEMO_PIN, DEMO_PIN, *commands)
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

    def test_rejects_nonpositive_or_unreadable_amounts(self):
        for value in ("0", "-50", "abc"):
            with self.subTest(value=value):
                output = self.session("2", value)
                self.assertIn("positive amount", output)
                self.assertNotIn("Remaining balance:", output)

    def test_login_allows_a_retry(self):
        result = invoke(DEMO_PIN, "9999", DEMO_PIN, "1")
        self.assertIn("Wrong PIN.", result.stdout)
        self.assertIn("Balance: 10000", result.stdout)

    def test_third_wrong_pin_ends_login(self):
        result = invoke(DEMO_PIN, "9999", "9999", "9999", DEMO_PIN, "1")
        self.assertIn("Too many attempts.", result.stdout)
        self.assertNotIn("Balance:", result.stdout)

    def test_change_accepts_a_leading_zero(self):
        self.assertIn("Pin changed successfully", self.session("3", DEMO_PIN, "0007", "0007"))

    def test_change_requires_a_different_four_digit_pin(self):
        for pin in ("123", "12345", "12a4", DEMO_PIN):
            with self.subTest(pin=pin):
                self.assertIn("different four-digit PIN", self.session("3", DEMO_PIN, pin))

    def test_fractional_withdrawal_uses_exact_cents(self):
        output = self.session("2", "0.09")
        self.assertIn("Withdrawal amount: 0.09", output)
        self.assertIn("Remaining balance: 9999.91", output)

    def test_does_not_round_excess_precision(self):
        self.assertIn("positive amount", self.session("2", "0.009"))

    def test_menu_consumes_one_complete_line(self):
        output = self.session("1 extra")
        self.assertIn("Invalid choice.", output)
        self.assertNotIn("Balance:", output)

    def test_trims_padding_and_carriage_returns(self):
        output = self.session("\t2\r", "  1.25\t\r")
        self.assertIn("Remaining balance: 9998.75", output)

    def test_extra_amount_tokens_are_not_a_valid_prefix(self):
        self.assertIn("positive amount", self.session("2", "1.25 extra"))

    def test_setup_reprompts_until_pin_is_well_formed(self):
        result = invoke("123", "12a4", DEMO_PIN, DEMO_PIN, "1")
        self.assertEqual(result.stdout.count("Use exactly four digits"), 2)
        self.assertIn("Balance: 10000.00", result.stdout)

    def test_pin_change_requires_matching_confirmation(self):
        output = self.session("3", DEMO_PIN, "0007", "0008")
        self.assertIn("confirmation did not match", output)
        self.assertNotIn("changed successfully", output)

    def test_wrong_current_pin_aborts_the_change(self):
        output = self.session("3", "9999")
        self.assertIn("PIN not changed.", output)
        self.assertNotIn("New PIN:", output)

    def test_one_login_supports_several_actions_until_exit(self):
        output = self.session("2", "10.01", "bad", "1", "0", "2", "5")
        self.assertIn("Invalid choice.", output)
        self.assertIn("Balance: 9989.99", output)
        self.assertEqual(output.count("Withdrawal amount:"), 1)

    def test_deposit_can_fund_a_later_withdrawal(self):
        output = self.session("4", "0.03", "2", "10000.02", "1", "0")
        self.assertIn("Deposit amount: 0.03", output)
        self.assertIn("Balance: 0.01", output)

    def test_deposit_overflow_does_not_change_balance(self):
        output = self.session("4", "184467440737095516.15", "1", "0")
        self.assertIn("exceed the balance limit", output)
        self.assertIn("Balance: 10000.00", output)
