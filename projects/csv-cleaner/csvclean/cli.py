import argparse
import json
import sys

from .rules import Rules
from .transform import CellEdits
from .layout import OptionError
from .cleaner import clean_table
from .streams import input_stream, output_stream
from .reader import Problem, audit


DIALECTS = {"comma": ",", "tab": "\t", "semicolon": ";", "pipe": "|"}


def source_options(command):
    command.add_argument("input", nargs="?", default="-", help="UTF-8 file or - for stdin")
    command.add_argument("--trim-header", action="store_true", help="strip names before duplicate checks")
    command.add_argument("--skip-blank", action="store_true", help="ignore empty physical records")
    command.add_argument("--delimiter", choices=DIALECTS, default="comma")


def rule_options(command):
    command.add_argument("--date", metavar="NAME", action="append", default=[], help="check ISO calendar dates")
    command.add_argument("--integer", metavar="NAME", action="append", default=[], help="check signed ASCII integer text")
    command.add_argument("--require", metavar="NAME", action="append", default=[], help="require a nonblank input value")


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
    rule_options(check)
    check.add_argument("--json", action="store_true", help="emit a structured report")
    check.add_argument("--max-errors", type=positive, default=1)
    clean = commands.add_parser("clean", help="write canonical CSV after checking each row")
    source_options(clean)
    rule_options(clean)
    clean.add_argument("--rename", nargs=2, metavar=("OLD", "NEW"), action="append", default=[])
    selection = clean.add_mutually_exclusive_group()
    selection.add_argument("--drop", metavar="NAME", action="append", default=[], help="omit a named column")
    selection.add_argument("--keep", metavar="NAME", action="append", default=[], help="keep a column in this order")
    clean.add_argument("--collapse-adjacent", action="store_true", help="skip consecutive identical output rows")
    clean.add_argument("--skip-empty", action="store_true", help="omit rows empty across selected cells before filling")
    clean.add_argument("--fill-empty", metavar="TEXT", help="replace empty output cells after trimming")
    clean.add_argument("--trim", action="store_true", help="strip outer whitespace from data cells")
    clean.add_argument("--output-delimiter", choices=DIALECTS, default="comma")
    clean.add_argument("--replace", action="store_true", help="allow atomic replacement of a different file")
    clean.add_argument("-o", "--output", default="-", help="new output path or - for stdout")
    return root


def main(argv=None, *, stdin=None, stdout=None, stderr=None):
    args = parser().parse_args(argv)
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    options = dict(delimiter=DIALECTS[args.delimiter], skip_blank=args.skip_blank,
                   trim_header=args.trim_header, rules=Rules(required=tuple(args.require), integer=tuple(args.integer), date=tuple(args.date)))
    try:
        with input_stream(args.input, stdin) as source:
            if args.command == "clean":
                with output_stream(args.output, stdout, replace=args.replace, input_path=args.input) as target:
                    clean_table(source, target, **options, output_delimiter=DIALECTS[args.output_delimiter],
                                edits=CellEdits(args.trim, args.fill_empty, args.skip_empty),
                                keep=args.keep, drop=args.drop, rename=args.rename, collapse=args.collapse_adjacent)
                return 0
            report = audit(source, **options, max_errors=args.max_errors)
    except Problem as exc:
        print(exc, file=stderr)
        return 1
    except OptionError as exc:
        print(exc, file=stderr)
        return 2
    except (OSError, UnicodeError) as exc:
        print(f"I/O or encoding error: {exc}", file=stderr)
        return 2
    if args.json:
        json.dump({"columns": report.header, "examined": report.examined, "stopped": report.stopped,
                   "issues": [{"first_line": e.first, "last_line": e.last, "message": e.message}
                              for e in report.problems]}, stdout, ensure_ascii=False)
        stdout.write("\n")
        return int(bool(report.problems))
    if report.problems:
        for issue in report.problems:
            print(issue, file=stderr)
        return 1
    print(f"OK: {report.examined} data rows, {len(report.header)} columns", file=stdout)
    return 0
