import argparse
import sys

from .availability import available
from .time import span


def interval_arg(text):
    try:
        return span(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def schedule_options(cmd):
    cmd.add_argument("--window", type=interval_arg, default=span("09:00-17:00"), metavar="START-END")
    cmd.add_argument("--busy", type=interval_arg, action="append", default=[], metavar="START-END")


def parser():
    root = argparse.ArgumentParser(prog="slotfind", description="Plan one local day in whole minutes.")
    commands = root.add_subparsers(dest="command", required=True)
    free = commands.add_parser("free", help="list shared free blocks")
    schedule_options(free)
    return root


def main(argv=None, *, stdout=None, stderr=None):
    args = parser().parse_args(argv)
    stdout = sys.stdout if stdout is None else stdout
    for block in available(args.window, args.busy):
        print(block, file=stdout)
    return 0
