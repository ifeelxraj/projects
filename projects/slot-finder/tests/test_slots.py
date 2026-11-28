import unittest

from slotfind.slots import candidates
from slotfind.time import Span


class CandidateTests(unittest.TestCase):
    def test_grid_starts_inside_gap_and_accepts_exact_fits(self):
        self.assertEqual(list(candidates([Span(3, 30), Span(31, 40)], 10, 10)), [Span(10, 20), Span(20, 30)])
        self.assertEqual(list(candidates([Span(1425, 1440)], 15, 15)), [Span(1425, 1440)])

    def test_nonpositive_durations_and_steps_have_no_valid_schedule(self):
        for duration, step in [(0, 1), (1, 0), (-1, 10)]:
            with self.assertRaises(ValueError):
                list(candidates([Span(0, 60)], duration, step))
