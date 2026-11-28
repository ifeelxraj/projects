import json
import subprocess
import unittest


class MorningTests(unittest.TestCase):
    def test_demo_offers_two_free_choices_nearest_ten(self):
        result = subprocess.run(["sh", "examples/shared-morning.sh"], capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [
            {"start": "10:00", "end": "10:30", "minutes": 30},
            {"start": "09:45", "end": "10:15", "minutes": 30}])
