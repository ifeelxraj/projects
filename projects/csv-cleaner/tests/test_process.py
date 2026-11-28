import subprocess
import sys
import unittest


def invoke(*args, data=b""):
    return subprocess.run([sys.executable, "-m", "csvclean", *args], input=data,
                          capture_output=True, timeout=5, check=False)


class PipeTests(unittest.TestCase):
    def test_utf8_signature_is_not_part_of_first_name(self):
        result = invoke("validate", data=b"\xef\xbb\xbfa,a\r\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"duplicate header", result.stderr)

    def test_invalid_bytes_do_not_become_replacement_text(self):
        result = invoke("validate", data=b"label\n\xff\n")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_checkout_launcher_resolves_inputs_in_the_callers_directory(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        script = Path(__file__).resolve().parents[1] / "csv-clean"
        with TemporaryDirectory() as d:
            (Path(d) / "local.csv").write_bytes(b"id\n01\n")
            result = subprocess.run([sys.executable, str(script), "validate", "local.csv"],
                                    cwd=d, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(b"1 data rows", result.stdout)
