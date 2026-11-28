import argparse
import sys

from .availability import available_across
from .slots import candidates
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
    slots = commands.add_parser("slots", help="list fixed-length meetings inside free blocks")
    schedule_options(slots)
    slots.add_argument("--duration", type=positive_minutes, required=True, metavar="MINUTES")
    slots.add_argument("--step", type=positive_minutes, default=15, metavar="MINUTES")
    return root


def main(argv=None, *, stdout=None, stderr=None):
    args = parser().parse_args(argv)
    stdout = sys.stdout if stdout is None else stdout
    busy = (period.padded(args.before, args.after) for period in args.busy)
    gaps = available_across(args.window or [span("09:00-17:00")], busy)
    if args.command == "free":
        blocks = (g for g in gaps if g.minutes >= args.min)
    else:
        blocks = candidates(gaps, args.duration, args.step)
    for block in blocks:
        print(block, file=stdout)
    return 0
