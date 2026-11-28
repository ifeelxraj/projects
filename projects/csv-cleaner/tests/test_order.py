import unittest

from test_cli import run


class OrderTests(unittest.TestCase):
    def test_composite_keys_use_textual_lexicographic_order(self):
        args = ("validate", "--order-by", "group", "--order-by", "code")
        self.assertEqual(run(*args, text="group,code\nA,10\nA,2\nA,2\nB,0")[0], 0)
        rc, _, err = run(*args, text="group,code\nB,1\nA,3")
        self.assertEqual(rc, 1)
        self.assertIn("line 3: sort key decreases", err)

    def test_strict_order_requires_a_key_and_rejects_duplicate_groups(self):
        text = "id,note\nalpha,x\nalpha,y\n"
        self.assertEqual(run("validate", "--strict-order", text=text)[0], 2)
        rc, _, err = run("clean", "--order-by", "id", "--strict-order", text=text)
        self.assertEqual(rc, 1)
        self.assertIn("line 3: duplicate ordered key", err)
