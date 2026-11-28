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
