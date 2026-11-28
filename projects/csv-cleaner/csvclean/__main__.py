import sys

from .csv_cleaner_commands import main


def entrypoint():
    # Pipes must use the same decoding and physical newline rules as named files.
    sys.stdin.reconfigure(encoding="utf-8-sig", errors="strict", newline="")
    sys.stdout.reconfigure(encoding="utf-8", errors="strict", newline="")
    return main()


if __name__ == "__main__":
    raise SystemExit(entrypoint())
