import subprocess
import sys
import unittest


def invoke(*args, data=b""):
    return subprocess.run([sys.executable, "-m", "slotfind", *args], input=data,
                          capture_output=True, timeout=5)


class ProcessTests(unittest.TestCase):
    def test_bad_calendar_data_and_bad_flags_have_different_exit_codes(self):
        for args, data, code in [(("free", "--calendar", "-"), b"resource,start,end\nX,24:01,24:00", 1),
                                 (("free", "--calendar", "-"), b"\xff", 2),
                                 (("free", "--window", "09:00-09:00"), b"", 2),
                                 (("slots", "--duration", "20", "--near", "10:00", "--non-overlap"), b"", 2)]:
            with self.subTest(args=args, data=data):
                result = invoke(*args, data=data)
                self.assertEqual((result.returncode, result.stdout), (code, b""))
                self.assertTrue(result.stderr)
                self.assertNotIn(b"Traceback", result.stderr)

    def test_bom_and_crlf_work_on_a_real_pipe(self):
        result = invoke("free", "--calendar", "-", data=b"\xef\xbb\xbfresource,start,end\r\nX,09:00,10:00\r\n")
        self.assertEqual((result.returncode, result.stdout), (0, b"10:00-17:00\n"))

    def test_standalone_launcher_reads_paths_relative_to_caller(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        script = Path(__file__).resolve().parents[1] / "slot-finder"
        with TemporaryDirectory() as d:
            (Path(d) / "bookings.csv").write_text("resource,start,end\nA,09:00,09:30", encoding="utf-8")
            result = subprocess.run([sys.executable, str(script), "free", "--calendar", "bookings.csv"],
                                    cwd=d, capture_output=True, timeout=5)
            self.assertEqual((result.returncode, result.stdout), (0, b"09:30-17:00\n"))
