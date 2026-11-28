import unittest

from test_cli import run


class LayoutTests(unittest.TestCase):
    def test_projection_uses_requested_order(self):
        rc, out, _ = run("clean", "--keep", "c", "--keep", "a", text="a,b,c\n1,2,3")
        self.assertEqual((rc, out), (0, "c,a\r\n3,1\r\n"))

    def test_unknown_and_repeated_names_do_not_emit_a_header(self):
        for args in [("--keep", "x"), ("--keep", "a", "--keep", "a")]:
            self.assertEqual(run("clean", *args, text="a,b\n1,2")[:2], (2, ""))

    def test_drop_preserves_order_and_does_not_mask_input_width_errors(self):
        args = ("clean", "--drop", "mid")
        self.assertEqual(run(*args, text="a,mid,b\n1,2,3")[1], "a,b\r\n1,3\r\n")
        self.assertEqual(run(*args, text="a,mid,b\n1,3")[0], 1)
        self.assertEqual(run("clean", "--drop", "a", text="a\n1")[0], 2)

    def test_renames_are_simultaneous_and_output_names_unique(self):
        sample = "a,b\n1,2"
        self.assertEqual(run("clean", "--rename", "a", "b", "--rename", "b", "a", text=sample)[1],
                         "b,a\r\n1,2\r\n")
        for args in [("--rename", "a", "b"), ("--drop", "b", "--rename", "b", "x")]:
            self.assertEqual(run("clean", *args, text=sample)[:2], (2, ""))
