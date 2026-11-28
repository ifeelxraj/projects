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
