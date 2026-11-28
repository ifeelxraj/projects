import sys

from .cli import main


def entrypoint():
    sys.stdin.reconfigure(encoding="utf-8-sig", errors="strict", newline="")
    sys.stdout.reconfigure(encoding="utf-8", newline="")
    return main()


if __name__ == "__main__":
    raise SystemExit(entrypoint())
