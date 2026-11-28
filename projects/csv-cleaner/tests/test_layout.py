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

    def test_fill_only_changes_empty_values_after_optional_trimming(self):
        sample = "a,b\n ,0\n,word"
        self.assertEqual(run("clean", "--fill-empty", "NA", text=sample)[1], "a,b\r\n ,0\r\nNA,word\r\n")
        self.assertEqual(run("clean", "--trim", "--fill-empty", "NA", text=sample)[1],
                         "a,b\r\nNA,0\r\nNA,word\r\n")

    def test_skip_empty_applies_to_output_columns_before_filling(self):
        rc, out, _ = run("clean", "--drop", "id", "--trim", "--skip-empty", "--fill-empty", "X",
                         text="id,a,b\n1, ,\n2,,value")
        self.assertEqual((rc, out), (0, "a,b\r\nX,value\r\n"))

    def test_adjacent_collapse_compares_emitted_values_not_source_rows(self):
        rc, out, _ = run("clean", "--keep", "v", "--trim", "--collapse-adjacent",
                         text="id,v\n1, x\n2,x\n3,y\n4,x")
        self.assertEqual((rc, out), (0, "v\r\nx\r\ny\r\nx\r\n"))

    def test_combined_pipeline_is_idempotent_on_canonical_output(self):
        args = ("clean", "--trim", "--trim-header", "--skip-empty", "--fill-empty", "unknown",
                "--collapse-adjacent")
        first = run(*args, text=' id ,note\n , \n01," a,b "\n01,"a,b"\n02,')
        self.assertEqual(first, (0, 'id,note\r\n01,"a,b"\r\n02,unknown\r\n', ""))
        self.assertEqual(run(*args, text=first[1]), first)

    def test_numbering_is_contiguous_after_filtering_and_collapse(self):
        cmd = ("clean", "--number-rows", "seq", "--skip-empty", "--collapse-adjacent")
        self.assertEqual(run(*cmd, text='v\nx\nx\n""\ny')[1], "seq,v\r\n1,x\r\n2,y\r\n")
        self.assertEqual(run(*cmd, text="seq\noriginal")[:2], (2, ""))
