import csv
import io
import itertools
import unittest

from csvclean.csv_cleaner_commands import DIALECTS
from test_csv_cleaner_commands import run


class RoundTripTests(unittest.TestCase):
    def test_every_delimiter_pair_preserves_difficult_cells(self):
        cells = ('', ' ', 'a,b', 'x;y', 'a|b', '\t', 'a"b', 'a\rb', '\r\n', '水🌱')
        expected = [("left", "right")] + list(itertools.product(cells, repeat=2))
        for name, sep in DIALECTS.items():
            source = io.StringIO(newline="")
            csv.writer(source, delimiter=sep).writerows(expected)
            for out_name, out_sep in DIALECTS.items():
                with self.subTest(source=name, target=out_name):
                    rc, text, err = run("clean", "--delimiter", name, "--output-delimiter", out_name,
                                        text=source.getvalue())
                    self.assertEqual((rc, err), (0, ""))
                    actual = csv.reader(io.StringIO(text, newline=""), delimiter=out_sep, strict=True)
                    self.assertEqual(list(map(tuple, actual)), expected)
