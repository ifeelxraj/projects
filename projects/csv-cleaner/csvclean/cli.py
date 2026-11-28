import argparse
import sys

from .reader import Problem, validate


def parser():
    root = argparse.ArgumentParser(prog="csvclean", description="Check and clean delimited tables.")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="check the header and every row width")
    return root


def main(argv=None, *, stdin=None, stdout=None, stderr=None):
    args = parser().parse_args(argv)
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    try:
        header, count = validate(stdin)
    except Problem as exc:
        print(exc, file=stderr)
        return 1
    print(f"OK: {count} data rows, {len(header)} columns", file=stdout)
    return 0
