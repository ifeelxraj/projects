import json
from pathlib import Path
import subprocess
import sys
import unittest


RECIPE = Path(__file__).resolve().parents[2] / "examples/availability/plan_export.py"


class ImportRecipeTests(unittest.TestCase):
    def invoke(self, args=(), data=b""):
        return subprocess.run([sys.executable, str(RECIPE), *args], input=data,
                              capture_output=True, timeout=10)

    def test_complete_fixture_produces_only_feasible_starts(self):
        run = self.invoke()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual([s["start"] for s in json.loads(run.stdout)], ["10:30", "11:30"])

    def test_bad_final_row_cannot_publish_a_partial_plan(self):
        run = self.invoke(["-"], b"Space\tFrom\tUntil\tState\nA\t09:00\t09:30\tbusy\nB\t10:00\n")
        self.assertEqual((run.returncode, run.stdout), (1, b""))
        self.assertIn(b"line 3", run.stderr)

    def test_calendar_semantics_are_checked_after_column_conversion(self):
        run = self.invoke(["-"], b"Space\tFrom\tUntil\tState\nA\t23:30\t00:30\tbusy\n")
        self.assertEqual((run.returncode, run.stdout), (1, b""))
        self.assertIn(b"start before its end", run.stderr)
