import io
import unittest

from slotfind.calendar import Booking, CalendarError, bookings
from slotfind.time import span


class CalendarTests(unittest.TestCase):
    def test_reordered_columns_extra_notes_and_quotes(self):
        data = 'note,end,resource,start\r\n"line 1\r\nline 2",10:00,"Room, A",09:30'
        self.assertEqual(list(bookings(io.StringIO(data, newline=""))), [Booking("Room, A", span("09:30-10:00"))])

    def test_bad_width_after_multiline_record_has_physical_location(self):
        data = 'resource,start,end,note\nR,09:00,10:00,"a\nb"\nR,09:45\n'
        with self.assertRaisesRegex(CalendarError, "demo.csv:4: expected 4 fields"):
            list(bookings(io.StringIO(data), "demo.csv"))
