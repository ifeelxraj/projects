import argparse
import sys

from .streams import input_stream
from .reader import Problem, validate


def parser():
    root = argparse.ArgumentParser(prog="csvclean", description="Check and clean delimited tables.")
    commands = root.add_subparsers(dest="command", required=True)
    check = commands.add_parser("validate", help="check the header and every row width")
    check.add_argument("input", nargs="?", default="-", help="UTF-8 file or - for stdin")
    return root


def main(argv=None, *, stdin=None, stdout=None, stderr=None):
    args = parser().parse_args(argv)
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    try:
        with input_stream(args.input, stdin) as source:
            header, count = validate(source)
    except Problem as exc:
        print(exc, file=stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print(f"input error: {exc}", file=stderr)
        return 2
    print(f"OK: {count} data rows, {len(header)} columns", file=stdout)
    return 0
