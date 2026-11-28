import io
import unittest

from slotfind.cli import main


def run(*args, text=""):
    out, err = io.StringIO(), io.StringIO()
    rc = main(args, stdin=io.StringIO(text, newline=""), stdout=out, stderr=err)
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

    def test_limit_applies_across_all_windows_in_chronological_order(self):
        args = ("slots", "--window", "14:00-15:00", "--window", "09:00-09:15", "--duration", "15")
        self.assertEqual(run(*args, "--limit", "2")[1], "09:00-09:15\n14:00-14:15\n")

    def test_nearest_ranking_precedes_limit_and_breaks_ties_earlier(self):
        rc, out, _ = run("slots", "--window", "10:00-11:00", "--step", "10", "--duration", "10",
                         "--near", "10:35", "--limit", "2")
        self.assertEqual((rc, out), (0, "10:30-10:40\n10:40-10:50\n"))

    def test_packing_returns_back_to_back_appointments_not_alternatives(self):
        rc, out, _ = run("slots", "--window", "10:00-11:00", "--step", "5", "--duration", "20", "--non-overlap")
        self.assertEqual((rc, out), (0, "10:00-10:20\n10:20-10:40\n10:40-11:00\n"))

    def test_json_has_explicit_endpoints_and_empty_list_for_no_fit(self):
        import json
        result = run("free", "--format", "json", "--window", "23:45-24:00")
        self.assertEqual(json.loads(result[1]), [{"start": "23:45", "end": "24:00", "minutes": 15}])
        self.assertEqual(json.loads(run("slots", "--duration", "24h", "--format", "json")[1]), [])

    def test_csv_is_headered_and_can_be_piped_to_other_tools(self):
        self.assertEqual(run("slots", "--duration", "1h", "--limit", "1", "--format", "csv")[1],
                         "start,end,minutes\n09:00,10:00,60\n")
        self.assertEqual(run("free", "--busy", "00:00-24:00", "--format", "csv")[1], "start,end,minutes\n")

    def test_require_match_signals_empty_results_without_changing_output_schema(self):
        for cmd in [("free",), ("slots", "--duration", "15"), ("rooms", "10:00-10:20")]:
            args = (*cmd, "--busy", "00:00-24:00", "--format", "json")
            self.assertEqual(run(*args), (0, "[]\n", ""))
            self.assertEqual(run(*args, "--require-match"), (3, "[]\n", ""))
        self.assertEqual(run("free", "--require-match")[0], 0)
