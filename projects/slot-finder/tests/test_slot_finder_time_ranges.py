import unittest

from slotfind.slot_finder_time_ranges import DAY, clock, minute


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
        from slotfind.slot_finder_time_ranges import span
        value = span("23:59-24:00")
        self.assertEqual((value.minutes, str(value)), (1, "23:59-24:00"))

    def test_empty_reversed_and_overnight_intervals_are_rejected(self):
        from slotfind.slot_finder_time_ranges import span
        for text in ("09:00-09:00", "22:00-03:30", "09:00-10:00-11:00", "24:00-24:00"):
            with self.assertRaises(ValueError):
                span(text)

    def test_touching_intervals_do_not_conflict(self):
        from slotfind.slot_finder_time_ranges import Span
        work = Span(60, 120)
        self.assertIsNone(work.intersect(Span(120, 140)))
        self.assertEqual(work.intersect(Span(30, 70)), Span(60, 70))
        self.assertTrue(work.contains(Span(60, 120)))
        self.assertFalse(work.contains(Span(90, 121)))


class DurationTests(unittest.TestCase):
    def test_duration_units_and_day_cap(self):
        from slotfind.slot_finder_time_ranges import duration_minutes
        for text, value in [("90", 90), ("90m", 90), ("1h30m", 90), ("24h", 1440), ("0m", 0)]:
            self.assertEqual(duration_minutes(text), value)
        for text in ("24h1m", "1h60m", "1.5h", "1:30", "-5", "2000m"):
            with self.assertRaises(ValueError):
                duration_minutes(text)

    def test_library_rejects_fractional_and_boolean_time_values_at_the_boundary(self):
        from slotfind.slot_finder_time_ranges import Span
        from slotfind.slot_finder_meeting_slots import candidates
        for value in (True, 1.5):
            with self.assertRaises(ValueError):
                Span(value, 5)
            with self.assertRaises(ValueError):
                clock(value)
            with self.assertRaises(ValueError):
                Span(1, 5).padded(value, 0)
            with self.assertRaises(ValueError):
                list(candidates([Span(1, 5)], value, 1))
