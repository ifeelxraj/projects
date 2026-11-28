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


class SpanTests(unittest.TestCase):
    def test_half_open_interval_can_end_at_midnight(self):
        from slotfind.time import span
        value = span("23:59-24:00")
        self.assertEqual((value.minutes, str(value)), (1, "23:59-24:00"))

    def test_empty_reversed_and_overnight_intervals_are_rejected(self):
        from slotfind.time import span
        for text in ("09:00-09:00", "22:00-03:30", "09:00-10:00-11:00", "24:00-24:00"):
            with self.assertRaises(ValueError):
                span(text)
