#!/usr/bin/env python3
"""Adapt a tab-delimited room export and plan only if the whole import succeeds."""

import argparse
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


HERE = Path(__file__).resolve().parent
PROJECTS = HERE.parents[1] / "projects"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", nargs="?", default=str(HERE / "vendor.tsv"))
    parser.add_argument("--window", default="09:00-12:00")
    parser.add_argument("--duration", default="30m")
    args = parser.parse_args()
    columns = {"Space": "resource", "From": "start", "Until": "end", "State": "status"}
    # A direct pipe could let the planner see valid-looking EOF on a prefix of
    # an export that failed validation. Publish a complete intermediate first.
    with TemporaryDirectory(prefix="plan-export-") as directory:
        calendar = str(Path(directory) / "calendar.csv")
        clean = [sys.executable, str(PROJECTS / "csv-cleaner/csv-cleaner"), "clean", args.export,
                 "--delimiter", "tab", "--trim-header", "--trim", "--output", calendar]
        for source, target in columns.items():
            clean.extend(["--keep", source, "--rename", source, target])
        for name in ("Space", "From", "Until"):
            clean.extend(["--require", name])
        checked = subprocess.run(clean, check=False)
        if checked.returncode:
            return checked.returncode
        return subprocess.run([sys.executable, str(PROJECTS / "slot-finder/find-slots"), "slots",
                               "--calendar", calendar, "--window", args.window, "--duration", args.duration,
                               "--format", "json"], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
