import io
import unittest

from csvclean.reader import Record, records


def source(text, **kwargs):
    return records(io.StringIO(text, newline=""), **kwargs)


class ReaderTests(unittest.TestCase):
    def test_quotes_and_source_spans(self):
        self.assertEqual(list(source('a,b\r\n"two,parts","two\r\nlines"\r\n')), [
            Record(1, 1, ("a", "b")), Record(2, 3, ("two,parts", "two\r\nlines"))])

    def test_stream_is_not_read_ahead_by_a_record(self):
        def lines():
            yield "first\n"
            raise AssertionError("read past requested record")
        self.assertEqual(next(records(lines())).fields, ("first",))


class HeaderTests(unittest.TestCase):
    def test_header_is_required_and_unambiguous(self):
        from csvclean.reader import Problem, read_header
        for text, message in [("", "missing header"), ("\n", "empty header"),
                              ("a, \n", "blank header"), ("a,a\n", "duplicate header")]:
            with self.subTest(text=text), self.assertRaisesRegex(Problem, message):
                read_header(source(text))
        self.assertEqual(read_header(source("Name,name\n")), ("Name", "name"))


class WidthTests(unittest.TestCase):
    def test_counts_data_records_not_physical_lines(self):
        from csvclean.reader import validate
        self.assertEqual(validate(io.StringIO('a,b\n1,"x\ny"\n2,z')), (("a", "b"), 2))

    def test_width_diagnostic_spans_entire_logical_record(self):
        from csvclean.reader import Problem, validate
        with self.assertRaisesRegex(Problem, "lines 2-3: expected 2 fields, found 1"):
            validate(io.StringIO('a,b\n"x\ny"\n'))


class DialectBoundaryTests(unittest.TestCase):
    def test_truncated_multiline_field_reports_its_record(self):
        from csvclean.reader import Problem
        with self.assertRaises(Problem) as caught:
            list(source('a,b\r\n0,"open\r\nstill open'))
        self.assertEqual((caught.exception.first, caught.exception.last), (2, 3))

    def test_blank_record_differs_from_an_empty_quoted_value(self):
        rows = list(source('\n""\n"a""b"'))
        self.assertEqual([r.fields for r in rows], [(), ("",), ('a"b',)])
