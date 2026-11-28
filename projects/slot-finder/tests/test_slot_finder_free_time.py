import unittest

from slotfind.slot_finder_free_time import union
from slotfind.slot_finder_time_ranges import Span


class UnionTests(unittest.TestCase):
    def test_union_merges_chains_nesting_and_duplicates_without_mutating_input(self):
        busy = [Span(8, 11), Span(2, 5), Span(5, 8), Span(3, 4), Span(8, 11), Span(20, 30)]
        original = busy[:]
        self.assertEqual(union(busy), [Span(2, 11), Span(20, 30)])
        self.assertEqual(busy, original)
        self.assertEqual(union([]), [])


class GapTests(unittest.TestCase):
    def test_clips_outside_bookings_and_keeps_both_edge_gaps(self):
        from slotfind.slot_finder_free_time import available
        window = Span(20, 60)
        self.assertEqual(available(window, [Span(5, 10), Span(30, 40), Span(70, 80)]),
                         [Span(20, 30), Span(40, 60)])
        self.assertEqual(available(window, [Span(5, 25), Span(50, 70)]), [Span(25, 50)])
        self.assertEqual(available(window, [Span(0, 90)]), [])

    def test_gap_algorithm_agrees_with_a_minute_occupancy_oracle(self):
        import random
        from slotfind.slot_finder_free_time import available
        rng = random.Random(137)
        for _ in range(300):
            window = Span(*sorted(rng.sample(range(61), 2)))
            busy = [Span(*sorted(rng.sample(range(61), 2))) for _ in range(rng.randrange(10))]
            expected = {m for m in range(window.start, window.end)
                        if not any(b.start <= m < b.end for b in busy)}
            gaps = available(window, busy)
            self.assertEqual({m for gap in gaps for m in range(gap.start, gap.end)}, expected)
            self.assertEqual(sum(g.minutes for g in gaps), len(expected))
            self.assertTrue(all(x.end < y.start for x, y in zip(gaps, gaps[1:])))

    def test_split_shifts_with_overlapping_windows_match_set_subtraction(self):
        import random
        from slotfind.slot_finder_free_time import available_across
        rng = random.Random(31)
        def sample():
            return [Span(*sorted(rng.sample(range(40), 2))) for _ in range(rng.randrange(7))]
        def minutes(spans):
            return {m for s in spans for m in range(s.start, s.end)}
        for _ in range(250):
            work, busy = sample(), sample()
            expected = minutes(work) - minutes(busy)
            gaps = available_across(work, busy)
            self.assertEqual(minutes(gaps), expected)
            self.assertEqual(sum(g.minutes for g in gaps), len(expected))
