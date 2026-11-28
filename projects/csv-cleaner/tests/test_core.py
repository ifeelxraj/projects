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
