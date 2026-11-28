import io
import unittest

from slotfind.slot_finder_calendar_reader import Booking, CalendarError, bookings
from slotfind.slot_finder_time_ranges import span


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
        from test_slot_finder_commands import run
        with TemporaryDirectory() as d:
            a, b = Path(d) / "a.csv", Path(d) / "b.csv"
            a.write_bytes(b"\xef\xbb\xbfresource,start,end\nA,09:00,09:30\n")
            b.write_bytes(b"resource,start,end\nB,09:40,10:00\n")
            result = run("free", "--window", "09:00-10:30", "--busy", "10:15-10:30", "--calendar", str(a), "--calendar", str(b))
            self.assertEqual(result, (0, "09:30-09:40\n10:00-10:15\n", ""))

    def test_stdin_calendar_can_only_be_consumed_once(self):
        from test_slot_finder_commands import run
        cmd = ("free", "--calendar", "-", "--window", "09:00-10:00")
        self.assertEqual(run(*cmd, text="resource,start,end\nA,09:00,09:45"), (0, "09:45-10:00\n", ""))
        self.assertEqual(run(*cmd, "--calendar", "-")[0], 2)

    def test_named_selection_does_not_remove_universal_manual_blocks(self):
        from test_slot_finder_commands import run
        data = "resource,start,end\nA,09:00,09:15\nB,09:30,09:45\n"
        cmd = ("free", "--window", "09:00-10:00", "--calendar", "-", "--busy", "09:55-10:00")
        self.assertEqual(run(*cmd, "--resource", "B", text=data)[1], "09:00-09:30\n09:45-09:55\n")
        rc, out, err = run(*cmd, "--resource", "missing", text=data)
        self.assertEqual((rc, out), (2, ""))
        self.assertIn("unknown resource", err)

    def test_free_or_cancelled_rows_do_not_block_but_still_name_a_resource(self):
        from test_slot_finder_commands import run
        data = "resource,start,end,status\nX,09:00,10:00,free\nX,10:00,11:00,CANCELLED\nX,11:00,12:00,tentative"
        args = ("free", "--resource", "X", "--calendar", "-", "--window", "09:00-12:00")
        self.assertEqual(run(*args, text=data)[1], "09:00-11:00\n")
        self.assertEqual(run(*args, text=data.replace("free", "typo"))[0], 1)

    def test_ignoring_tentative_bookings_never_unblocks_confirmed_time(self):
        from test_slot_finder_commands import run
        data = "resource,start,end,status\nA,09:00,10:00,tentative\nB,09:30,09:45,busy"
        args = ("free", "--calendar", "-", "--window", "09:00-10:00")
        self.assertEqual(run(*args, text=data)[1], "")
        self.assertEqual(run(*args, "--ignore-tentative", text=data)[1], "09:00-09:30\n09:45-10:00\n")

    def test_selecting_from_a_one_pass_import_does_not_exhaust_it_twice(self):
        from slotfind.slot_finder_calendar_reader import select_bookings
        text = "resource,start,end\nA,09:00,10:00\nB,10:00,11:00"
        entries = bookings(io.StringIO(text))
        self.assertEqual(select_bookings(entries, ["B"]), [Booking("B", span("10:00-11:00"))])
        self.assertEqual(len(select_bookings(bookings(io.StringIO(text)), [])), 2)
