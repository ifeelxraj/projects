import sys

from .cli import main

# Pipes must use the same decoding and physical newline rules as named files.
sys.stdin.reconfigure(encoding="utf-8-sig", errors="strict", newline="")
sys.stdout.reconfigure(encoding="utf-8", errors="strict", newline="")
raise SystemExit(main())
