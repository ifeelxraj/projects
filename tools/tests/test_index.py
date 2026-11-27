import unittest

from tools.check_index import index_errors


class IndexTests(unittest.TestCase):
    def test_folder_and_readme_links_both_count(self):
        table = "| Project | Status |\n| [A](projects/a/) | Active |\n| [B](./projects/b/README.md) | Complete |"
        self.assertEqual(index_errors(table, {"a": True, "b": True}), [])

    def test_flags_missing_docs_stale_links_and_unlisted_projects(self):
        table = "| Project | Status |\n| [A](projects/a/) | Active |\n| [B](projects/b/) | Complete |"
        errors = index_errors(table, {"a": False, "c": True})
        self.assertIn("projects/a/ needs a nonempty README.md", errors)
        self.assertIn("README.md:3: no projects/b/ directory", errors)
        self.assertIn("projects/c/ is missing from the table", errors)

    def test_empty_status_and_duplicate_rows(self):
        table = "| Project | Type | Status |\n| [A](projects/a/) | Demo ||\n| [Again](projects/a/) | Demo | Ready |"
        errors = index_errors(table, {"a": True})
        self.assertIn("README.md:2: missing status for a", errors)
        self.assertIn("README.md:3: duplicate project a", errors)

    def test_a_description_cannot_stand_in_for_a_missing_status_cell(self):
        table = "| Project | Description | Status |\n| [A](projects/a/) | Works locally |"
        self.assertEqual(index_errors(table, {"a": True}), ["README.md:2: missing status for a"])

    def test_status_column_need_not_be_last(self):
        table = "| Project | Status | Language |\n| [A](projects/a/) | Active | |"
        self.assertEqual(index_errors(table, {"a": True}), [])
