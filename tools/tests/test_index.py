import unittest

from tools.check_index import index_errors


class IndexTests(unittest.TestCase):
    def test_folder_and_readme_links_both_count(self):
        table = "| [A](projects/a/) | Active |\n| [B](./projects/b/README.md) | Complete |"
        self.assertEqual(index_errors(table, {"a": True, "b": True}), [])

    def test_flags_missing_docs_stale_links_and_unlisted_projects(self):
        table = "| [A](projects/a/) | Active |\n| [B](projects/b/) | Complete |"
        errors = index_errors(table, {"a": False, "c": True})
        self.assertIn("projects/a/ needs a nonempty README.md", errors)
        self.assertIn("README.md:2: no projects/b/ directory", errors)
        self.assertIn("projects/c/ is missing from the table", errors)

    def test_empty_status_and_duplicate_rows(self):
        table = "| [A](projects/a/) | Demo |  |\n| [Again](projects/a/) | Ready |"
        errors = index_errors(table, {"a": True})
        self.assertIn("README.md:1: missing status for a", errors)
        self.assertIn("README.md:2: duplicate project a", errors)
