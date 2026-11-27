#!/usr/bin/env python3
"""Check that projects/ and the root README's project table agree."""

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_LINK = re.compile(r"\[[^\]]+\]\((?:\./)?projects/([^/()\s]+)(?:/(?:README\.md)?)?\)")


def index_errors(markdown, has_readme):
    """Use the named Status column, not an arbitrary last nonempty cell."""
    errors = []
    listed = set()
    status_col = None
    for number, line in enumerate(markdown.splitlines(), 1):
        row = line.strip()
        if not row.startswith("|"):
            status_col = None
            continue
        body = row[1:]
        if body.endswith("|"):
            body = body[:-1]
        cells = [part.strip() for part in body.split("|")]
        if cells[0].casefold() == "project":
            headings = [cell.casefold() for cell in cells]
            status_col = headings.index("status") if "status" in headings else None
            continue
        link = PROJECT_LINK.fullmatch(cells[0])
        if not link:
            continue
        name = link.group(1)
        if name in listed:
            errors.append(f"README.md:{number}: duplicate project {name}")
        listed.add(name)
        if name not in has_readme:
            errors.append(f"README.md:{number}: no projects/{name}/ directory")
        if status_col is None or status_col >= len(cells) or not cells[status_col]:
            errors.append(f"README.md:{number}: missing status for {name}")

    for name in sorted(has_readme):
        if not has_readme[name]:
            errors.append(f"projects/{name}/ needs a nonempty README.md")
        if name not in listed:
            errors.append(f"projects/{name}/ is missing from the table")
    return errors


def main():
    projects = ROOT / "projects"
    has_readme = {}
    for path in projects.iterdir():
        if path.is_dir() and not path.name.startswith("."):
            doc = path / "README.md"
            has_readme[path.name] = doc.is_file() and bool(doc.read_text(encoding="utf-8").strip())
    errors = index_errors((ROOT / "README.md").read_text(encoding="utf-8"), has_readme)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Project index OK ({len(has_readme)} listed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
