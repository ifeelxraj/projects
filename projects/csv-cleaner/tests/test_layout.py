import unittest

from test_cli import run


class LayoutTests(unittest.TestCase):
    def test_projection_uses_requested_order(self):
        rc, out, _ = run("clean", "--keep", "c", "--keep", "a", text="a,b,c\n1,2,3")
        self.assertEqual((rc, out), (0, "c,a\r\n3,1\r\n"))

    def test_unknown_and_repeated_names_do_not_emit_a_header(self):
        for args in [("--keep", "x"), ("--keep", "a", "--keep", "a")]:
            self.assertEqual(run("clean", *args, text="a,b\n1,2")[:2], (2, ""))
