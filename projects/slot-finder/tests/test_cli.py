import io
import unittest

from slotfind.cli import main


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    rc = main(args, stdout=out, stderr=err)
    return rc, out.getvalue(), err.getvalue()


class FreeTests(unittest.TestCase):
    def test_default_workday_and_repeated_busy_flags(self):
        self.assertEqual(run("free"), (0, "09:00-17:00\n", ""))
        self.assertEqual(run("free", "--window", "10:00-12:00", "--busy", "10:15-11:00",
                             "--busy", "11:00-11:30")[1], "10:00-10:15\n11:30-12:00\n")
