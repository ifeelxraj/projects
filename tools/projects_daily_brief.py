#!/usr/bin/env python3
"""Print a read-only, UTC start-of-run brief for this checkout."""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).rstrip()


def relevant_handoffs(paths, today):
    """Show the latest earlier handoff (if any), then this day's prior runs."""
    dated = {}
    for path in paths:
        try:
            stamp = date.fromisoformat(path.stem)
        except ValueError:
            continue
        if path.name == f"{stamp.isoformat()}.md":
            dated[stamp] = path
    previous = max((day for day in dated if day < today), default=None)
    return [dated[day] for day in (previous, today) if day in dated]


def section(title, body):
    print(f"\n--- {title} ---\n{body}")


def main():
    today = datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)
    print(f"Daily run brief | {today} UTC\nStart revision: {git('rev-parse', 'HEAD')}")
    section("Working tree", git("status", "--short", "--branch"))
    section("Project index", (ROOT / "README.md").read_text(encoding="utf-8").strip())
    section("Recent history", git("log", "-12", "--format=%h %cs %s"))
    history = git("log", f"--since={yesterday}T00:00:00+00:00",
                  f"--until={yesterday}T23:59:59+00:00", "--format=%h %s")
    section(f"{yesterday} UTC commits", history or "None in the available branch history.")
    handoffs = relevant_handoffs((ROOT / "logs").glob("*.md"), today)
    for path in handoffs:
        section(f"Handoff: {path.name}", path.read_text(encoding="utf-8").strip())
    if not handoffs:
        section("Handoffs", "No current or earlier dated logs in this checkout.")


if __name__ == "__main__":
    main()
