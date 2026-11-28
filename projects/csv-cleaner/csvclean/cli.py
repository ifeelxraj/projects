import argparse
import sys

from .streams import input_stream
from .reader import Problem, audit


DIALECTS = {"comma": ",", "tab": "\t", "semicolon": ";", "pipe": "|"}


def source_options(command):
    command.add_argument("input", nargs="?", default="-", help="UTF-8 file or - for stdin")
    command.add_argument("--skip-blank", action="store_true", help="ignore empty physical records")
    command.add_argument("--delimiter", choices=DIALECTS, default="comma")


def positive(text):
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def parser():
    root = argparse.ArgumentParser(prog="csvclean", description="Check and clean delimited tables.")
    commands = root.add_subparsers(dest="command", required=True)
    check = commands.add_parser("validate", help="check the header and every row width")
    source_options(check)
    check.add_argument("--max-errors", type=positive, default=1)
    return root


def main(argv=None, *, stdin=None, stdout=None, stderr=None):
    args = parser().parse_args(argv)
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    try:
        with input_stream(args.input, stdin) as source:
            report = audit(source, DIALECTS[args.delimiter], skip_blank=args.skip_blank,
                           max_errors=args.max_errors)
    except Problem as exc:
        print(exc, file=stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print(f"input error: {exc}", file=stderr)
        return 2
    if report.problems:
        for issue in report.problems:
            print(issue, file=stderr)
        return 1
    print(f"OK: {report.examined} data rows, {len(report.header)} columns", file=stdout)
    return 0
