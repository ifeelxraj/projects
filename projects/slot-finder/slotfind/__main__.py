import sys

from .cli import main

if __name__ == "__main__":
    sys.stdin.reconfigure(encoding="utf-8-sig", errors="strict", newline="")
    sys.stdout.reconfigure(encoding="utf-8", newline="")
    raise SystemExit(main())
