import io
import unittest

from csvclean.cli import main


def run(*args, text=""):
    out, err = io.StringIO(newline=""), io.StringIO()
    status = main(args, stdin=io.StringIO(text, newline=""), stdout=out, stderr=err)
    return status, out.getvalue(), err.getvalue()


class ValidateTests(unittest.TestCase):
    def test_valid_stdin(self):
        self.assertEqual(run("validate", text="a,b\n1,2\n"), (0, "OK: 1 data rows, 2 columns\n", ""))

    def test_invalid_input_has_data_exit_status(self):
        rc, out, err = run("validate", text="a,b\n1\n")
        self.assertEqual((rc, out), (1, ""))
        self.assertIn("line 2", err)

    def test_file_argument_and_missing_file_diagnostic(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            rc, _, err = run("validate", str(path))
            self.assertEqual(rc, 2)
            self.assertIn("I/O or encoding error", err)
            path.write_bytes(b"a,b\r\n1,2\r\n")
            self.assertEqual(run("validate", str(path))[0], 0)

    def test_explicit_delimiters_respect_quoting(self):
        for name, sep in [("semicolon", ";"), ("tab", "\t"), ("pipe", "|")]:
            with self.subTest(name=name):
                rc, out, _ = run("validate", "--delimiter", name, text=f'a{sep}b\n"x{sep}y"{sep}z')
                self.assertEqual(rc, 0)
                self.assertIn("2 columns", out)

    def test_skip_blank_does_not_skip_quoted_empty_values(self):
        rc, out, _ = run("validate", "--skip-blank", text='\nlabel\n\n""\n')
        self.assertEqual(rc, 0)
        self.assertIn("1 data rows", out)
        self.assertEqual(run("validate", text="label\n\n")[0], 1)

    def test_bounded_diagnostics_stop_at_the_requested_number(self):
        rc, _, err = run("validate", "--max-errors", "2", text="a,b\n1\n2,ok\n3,x,y\n4\n")
        self.assertEqual(rc, 1)
        self.assertIn("line 2:", err)
        self.assertIn("line 4:", err)
        self.assertNotIn("line 5:", err)

    def test_json_report_keeps_coordinates_separate_from_messages(self):
        import json
        rc, out, err = run("validate", "--json", text='id,note\n1,ok\n"x\ny"\n')
        data = json.loads(out)
        self.assertEqual((rc, err, data["examined"], data["stopped"]), (1, "", 2, True))
        self.assertEqual(data["columns"], ["id", "note"])
        self.assertEqual(data["issues"], [{"first_line": 3, "last_line": 4,
                                           "message": "expected 2 fields, found 1"}])


class CleanerTests(unittest.TestCase):
    def test_normalizes_record_endings_without_changing_cell_text(self):
        rc, out, err = run("clean", text='a,b\n"1",two\n2,"x\ry"\n3,"a,b"')
        self.assertEqual((rc, err), (0, ""))
        self.assertEqual(out, 'a,b\r\n1,two\r\n2,"x\ry"\r\n3,"a,b"\r\n')

    def test_stdout_can_contain_valid_prefix_before_a_late_error(self):
        rc, out, err = run("clean", text="a,b\n1,2\n3\n")
        self.assertEqual((rc, out), (1, "a,b\r\n1,2\r\n"))
        self.assertIn("line 3", err)

    def test_transcodes_separators_and_requotes_the_new_separator(self):
        rc, out, _ = run("clean", "--delimiter", "semicolon", "--output-delimiter", "tab",
                         text='key;note\na;"x;y"\nb;has\ttab\n')
        self.assertEqual((rc, out), (0, 'key\tnote\r\na\tx;y\r\nb\t"has\ttab"\r\n'))

    def test_trim_is_opt_in_and_preserves_internal_spaces(self):
        sample = " label ,unit\n  two  words , kg \n"
        self.assertIn("  two  words , kg ", run("clean", text=sample)[1])
        self.assertEqual(run("clean", "--trim", text=sample)[1], " label ,unit\r\ntwo  words,kg\r\n")

    def test_header_cleanup_checks_collisions_before_writing(self):
        self.assertEqual(run("clean", "--trim-header", text=" a ,b \n x ,y")[1], "a,b\r\n x ,y\r\n")
        for command in ("clean", "validate"):
            rc, out, err = run(command, "--trim-header", text=" id,id \n1,2")
            self.assertEqual((rc, out), (1, ""))
            self.assertIn("duplicate header", err)
