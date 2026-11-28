import unittest

from slotfind.availability import union
from slotfind.time import Span


class UnionTests(unittest.TestCase):
    def test_union_merges_chains_nesting_and_duplicates_without_mutating_input(self):
        busy = [Span(8, 11), Span(2, 5), Span(5, 8), Span(3, 4), Span(8, 11), Span(20, 30)]
        original = busy[:]
        self.assertEqual(union(busy), [Span(2, 11), Span(20, 30)])
        self.assertEqual(busy, original)
        self.assertEqual(union([]), [])


class GapTests(unittest.TestCase):
    def test_clips_outside_bookings_and_keeps_both_edge_gaps(self):
        from slotfind.availability import available
        window = Span(20, 60)
        self.assertEqual(available(window, [Span(5, 10), Span(30, 40), Span(70, 80)]),
                         [Span(20, 30), Span(40, 60)])
        self.assertEqual(available(window, [Span(5, 25), Span(50, 70)]), [Span(25, 50)])
        self.assertEqual(available(window, [Span(0, 90)]), [])
