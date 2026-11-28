import unittest

from slotfind.time import DAY, clock, minute


class ClockTests(unittest.TestCase):
    def test_round_trip_entire_day_including_terminal_midnight(self):
        for value in range(DAY + 1):
            self.assertEqual(minute(clock(value)), value)

    def test_rejects_ambiguous_or_out_of_day_text(self):
        for text in ("9:15", "24:01", "12:60", "１２:３４", "09:00Z", "00:00:00"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                minute(text)
