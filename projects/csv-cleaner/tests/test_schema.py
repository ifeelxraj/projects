import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from test_cli import run


class SchemaTests(unittest.TestCase):
    def check(self, schema, text, *extra):
        with TemporaryDirectory() as d:
            path = Path(d) / "schema.json"
            path.write_text(json.dumps(schema), encoding="utf-8")
            return run("validate", "--schema", str(path), *extra, text=text)

    def test_schema_and_cli_rules_are_additive(self):
        schema = {"version": 1, "integer": ["n"]}
        self.assertEqual(self.check(schema, "n,id\n5,a", "--require", "id")[0], 0)
        self.assertEqual(self.check(schema, "n,id\n5,", "--require", "id")[0], 1)
        self.assertEqual(self.check(schema, "n,id\nx,a", "--require", "id")[0], 1)

    def test_invalid_config_is_not_mistaken_for_bad_data(self):
        for spec in [{}, {"version": True}, {"version": 1, "typo": []},
                     {"version": 1, "integer": "count"}, {"version": 1, "required": ["a", "a"]}]:
            self.assertEqual(self.check(spec, "a\n1")[0], 2)

    def test_optional_column_contract_detects_schema_drift(self):
        schema = {"version": 1, "columns": ["a", "b"]}
        for header in ("b,a", "a", "a,b,c", "x,b"):
            self.assertEqual(self.check(schema, header)[0], 1)
        self.assertEqual(self.check(schema, " a ,b", "--trim-header")[0], 0)
        self.assertEqual(self.check({"version": 1, "columns": []}, "x")[0], 2)

    def test_generated_template_round_trips_without_sampling_values(self):
        rc, out, err = run("schema", text="id,city\nnot,sampled,here\n")
        self.assertEqual((rc, err), (0, ""))
        self.assertNotIn("sampled", out)
        self.assertEqual(self.check(json.loads(out), "id,city\n1,Demo")[0], 0)

    def test_duplicate_json_keys_cannot_silently_disable_a_check(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "duplicate.json"
            path.write_text('{"version":1,"required":["id"],"required":[]}', encoding="utf-8")
            rc, _, err = run("clean", "--schema", str(path), text="id\n42")
            self.assertEqual(rc, 2)
            self.assertIn("duplicate schema key", err)
