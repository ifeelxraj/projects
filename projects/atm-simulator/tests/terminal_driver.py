import os
from pathlib import Path
import subprocess


DEFAULT_BINARY = Path(__file__).resolve().parents[1] / "build" / "atm"
BINARY = Path(os.environ.get("ATM_BINARY", DEFAULT_BINARY))
DEMO_PIN = "0042"  # Made-up for this in-memory test account.


def invoke(*lines, args=()):
    return subprocess.run(
        [str(BINARY), *args],
        input="".join(line + "\n" for line in lines),
        capture_output=True,
        text=True,
        timeout=3,
        check=False,
    )
