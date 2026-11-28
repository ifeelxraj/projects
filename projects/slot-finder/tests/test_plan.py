import unittest

from slotfind.calendar import Booking
from slotfind.plan import prepare
from slotfind.time import Span


class PlanTests(unittest.TestCase):
    def test_retains_source_labels_and_nonblocking_resources(self):
        plan = prepare([Span(0, 90)], [Span(1, 2)], [Booking("B", Span(5, 10)), Booking("A", Span(0, 5), "free")],
                       after=1)
        self.assertEqual(plan.resources, ("A", "B"))
        self.assertEqual([b.resource for b in plan.blockers], [None, "B"])
        self.assertEqual(plan.gaps, (Span(0, 1), Span(3, 5), Span(11, 90)))

    def test_summary_counts_overlapping_bookings_and_work_only_once(self):
        import json
        from test_cli import run
        rc, out, _ = run("summary", "--window", "09:00-10:00", "--window", "09:30-11:00",
                         "--busy", "08:00-09:30", "--busy", "09:15-09:45", "--format", "json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), {"work_minutes": 120, "busy_minutes": 45, "free_minutes": 75,
                                           "free_blocks": 1, "longest_free_minutes": 75})
