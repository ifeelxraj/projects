import io
import unittest

from slotfind.cli import main


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    rc = main(args, stdout=out, stderr=err)
    return rc, out.getvalue(), err.getvalue()


class FreeTests(unittest.TestCase):
    def test_default_workday_and_repeated_busy_flags(self):
        self.assertEqual(run("free"), (0, "09:00-17:00\n", ""))
        self.assertEqual(run("free", "--window", "10:00-12:00", "--busy", "10:15-11:00",
                             "--busy", "11:00-11:30")[1], "10:00-10:15\n11:30-12:00\n")

    def test_minimum_free_block_is_inclusive(self):
        self.assertEqual(run("free", "--window", "10:00-11:00", "--busy", "10:14-10:45", "--min", "15")[1],
                         "10:45-11:00\n")

    def test_setup_and_cleanup_buffers_clip_at_day_boundaries(self):
        self.assertEqual(run("free", "--window", "00:00-24:00", "--busy", "00:01-01:00",
                             "--busy", "23:00-23:59", "--before", "10", "--after", "5")[1],
                         "01:05-22:50\n")

    def test_multiple_work_windows_leave_lunch_unavailable(self):
        self.assertEqual(run("free", "--window", "09:00-12:00", "--window", "13:00-17:00",
                             "--busy", "11:45-13:20")[1], "09:00-11:45\n13:20-17:00\n")


class SlotTests(unittest.TestCase):
    def test_slots_may_overlap_each_other_but_not_a_booking(self):
        rc, out, _ = run("slots", "--duration", "20", "--step", "10", "--window", "09:00-10:00",
                         "--busy", "09:30-09:40")
        self.assertEqual((rc, out), (0, "09:00-09:20\n09:10-09:30\n09:40-10:00\n"))

    def test_grid_reference_does_not_reset_at_each_busy_period(self):
        rc, out, _ = run("slots", "--duration", "10", "--step", "20", "--anchor", "09:05",
                         "--window", "09:00-10:00", "--busy", "09:18-09:27")
        self.assertEqual((rc, out), (0, "09:05-09:15\n09:45-09:55\n"))
