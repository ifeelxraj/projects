import json
import unittest

from test_cli import run


class ProfileTests(unittest.TestCase):
    def test_counts_empty_and_whitespace_separately_in_code_points(self):
        rc, out, err = run("profile", text="id,note\n1,\n2,  \n3,水🌱\n")
        self.assertEqual((rc, err), (0, ""))
        self.assertNotIn("水", out)
        stats = json.loads(out)
        self.assertEqual(stats["rows"], 3)
        self.assertEqual(stats["columns"][1], {"name": "note", "empty": 1, "whitespace_only": 1, "max_chars": 2})

    def test_failing_profiles_do_not_publish_partial_results(self):
        self.assertEqual(run("profile", text="a,b\n1,2\n3")[:2], (1, ""))
