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
