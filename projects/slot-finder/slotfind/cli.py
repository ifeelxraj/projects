import argparse
import sys

from .availability import available_across
from .time import span


def interval_arg(text):
    try:
        return span(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def positive_minutes(text):
    value = int(text)
    if not 1 <= value <= 1440:
        raise argparse.ArgumentTypeError("expected 1 to 1440 minutes")
    return value


def nonnegative_minutes(text):
    value = int(text)
    if not 0 <= value <= 1440:
        raise argparse.ArgumentTypeError("expected 0 to 1440 minutes")
    return value


def schedule_options(cmd):
    cmd.add_argument("--before", type=nonnegative_minutes, default=0, help="setup minutes before each booking")
    cmd.add_argument("--after", type=nonnegative_minutes, default=0, help="cleanup minutes after each booking")
    cmd.add_argument("--window", type=interval_arg, action="append", default=[], metavar="START-END")
    cmd.add_argument("--busy", type=interval_arg, action="append", default=[], metavar="START-END")


def parser():
    root = argparse.ArgumentParser(prog="slotfind", description="Plan one local day in whole minutes.")
    commands = root.add_subparsers(dest="command", required=True)
    free = commands.add_parser("free", help="list shared free blocks")
    schedule_options(free)
    free.add_argument("--min", type=positive_minutes, default=1, metavar="MINUTES", help="minimum useful free block")
    return root


def main(argv=None, *, stdout=None, stderr=None):
    args = parser().parse_args(argv)
    stdout = sys.stdout if stdout is None else stdout
    busy = (period.padded(args.before, args.after) for period in args.busy)
    for block in available_across(args.window or [span("09:00-17:00")], busy):
        if block.minutes >= args.min:
            print(block, file=stdout)
    return 0
