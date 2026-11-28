import argparse
from contextlib import nullcontext
from itertools import islice
import sys

from .calendar import CalendarError, SelectionError, bookings, select_bookings
from .availability import available_across
from .output import write_blocks
from .slots import candidates, non_overlapping
from .time import duration_minutes, minute, span


def interval_arg(text):
    try:
        return span(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def positive_minutes(text):
    value = nonnegative_minutes(text)
    if not 1 <= value <= 1440:
        raise argparse.ArgumentTypeError("expected 1 to 1440 minutes")
    return value


def nonnegative_minutes(text):
    try:
        return duration_minutes(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def result_limit(text):
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("the result limit must be positive")
    return min(value, 1440)  # At most one distinct start per minute.


def schedule_options(cmd):
    cmd.add_argument("--format", choices=("text", "json", "csv"), default="text")
    cmd.add_argument("--resource", action="append", default=[], metavar="NAME", help="only include selected resources")
    cmd.add_argument("--calendar", action="append", default=[], metavar="FILE", help="read a local booking CSV")
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
    ordering = slots.add_mutually_exclusive_group()
    ordering.add_argument("--non-overlap", action="store_true", help="pack nonoverlapping meetings chronologically")
    ordering.add_argument("--near", type=minute, metavar="HH:MM", help="prefer starts nearest this time")
    slots.add_argument("--limit", type=result_limit, metavar="N", help="emit at most N slots")
    slots.add_argument("--anchor", type=minute, default=0, metavar="HH:MM", help="grid reference time (default midnight)")
    slots.add_argument("--step", type=positive_minutes, default=15, metavar="MINUTES")
    return root


def main(argv=None, *, stdin=None, stdout=None, stderr=None):
    args = parser().parse_args(argv)
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    stdin = sys.stdin if stdin is None else stdin
    if args.calendar.count("-") > 1:
        print("stdin can only be used once", file=stderr)
        return 2
    entries = []
    periods = list(args.busy)
    try:
        for path in args.calendar:
            handle = nullcontext(stdin) if path == "-" else open(path, encoding="utf-8-sig", newline="")
            with handle as stream:
                entries.extend(bookings(stream, path))
        periods.extend(b.interval for b in select_bookings(entries, args.resource) if b.blocks())
    except SelectionError as exc:
        print(exc, file=stderr)
        return 2
    except CalendarError as exc:
        print(exc, file=stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print(f"calendar input: {exc}", file=stderr)
        return 2
    busy = (period.padded(args.before, args.after) for period in periods)
    gaps = available_across(args.window or [span("09:00-17:00")], busy)
    if args.command == "free":
        blocks = (g for g in gaps if g.minutes >= args.min)
    else:
        blocks = candidates(gaps, args.duration, args.step, args.anchor)
        if args.near is not None:
            blocks = sorted(blocks, key=lambda block: (abs(block.start - args.near), block.start))
        if args.non_overlap:
            blocks = non_overlapping(blocks)
        if args.limit is not None:
            blocks = islice(blocks, args.limit)
    write_blocks(blocks, args.format, stdout)
    return 0
