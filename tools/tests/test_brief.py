from datetime import date
from pathlib import Path
import unittest

from tools.run_brief import relevant_handoffs


class RunBriefTests(unittest.TestCase):
    day = date(2026, 11, 27)

    def test_selects_previous_workday_and_same_day_runs(self):
        files = [Path(f"2026-11-{n}.md") for n in (28, 20, 27, 24)]
        self.assertEqual(relevant_handoffs(files, self.day), [files[3], files[2]])

    def test_future_and_non_daily_notes_do_not_look_like_prior_work(self):
        files = [Path(name) for name in ("README.md", "2026-02-30.md", "2026-12-01.md")]
        self.assertEqual(relevant_handoffs(files, self.day), [])
