import json
import subprocess
import unittest


class RecipeTests(unittest.TestCase):
    def test_stock_recipe_preserves_identifiers_and_reconciles_counts(self):
        run = subprocess.run(["sh", "examples/csv-cleaner-stock-demo.sh"], capture_output=True, timeout=5)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, b"seq,item,units,note\r\n1,bolts,03,pack; small\r\n2,washers,2,unknown\r\n")
        self.assertEqual(json.loads(run.stderr)["collapsed"], 1)
