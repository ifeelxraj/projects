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

    def test_multiple_export_files_and_manual_blocks_are_combined(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from test_cli import run
        with TemporaryDirectory() as d:
            a, b = Path(d) / "a.csv", Path(d) / "b.csv"
            a.write_bytes(b"\xef\xbb\xbfresource,start,end\nA,09:00,09:30\n")
            b.write_bytes(b"resource,start,end\nB,09:40,10:00\n")
            result = run("free", "--window", "09:00-10:30", "--busy", "10:15-10:30", "--calendar", str(a), "--calendar", str(b))
            self.assertEqual(result, (0, "09:30-09:40\n10:00-10:15\n", ""))

    def test_stdin_calendar_can_only_be_consumed_once(self):
        from test_cli import run
        cmd = ("free", "--calendar", "-", "--window", "09:00-10:00")
        self.assertEqual(run(*cmd, text="resource,start,end\nA,09:00,09:45"), (0, "09:45-10:00\n", ""))
        self.assertEqual(run(*cmd, "--calendar", "-")[0], 2)
