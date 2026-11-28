"""Import local calendar exports; do not require account credentials or APIs."""

import csv
from dataclasses import dataclass

from .time import Span, minute


class CalendarError(ValueError):
    pass


@dataclass(frozen=True)
class Booking:
    resource: str
    interval: Span
    status: str = "busy"

    def blocks(self, *, ignore_tentative=False):
        return self.status == "busy" or (self.status == "tentative" and not ignore_tentative)


def located_rows(stream, source):
    reader = csv.reader(stream, strict=True)
    while True:
        first = reader.line_num + 1
        try:
            values = next(reader)
        except StopIteration:
            return
        except csv.Error as exc:
            raise CalendarError(f"{source}:{first}: {exc}") from exc
        if values:
            location = str(first) if first == reader.line_num else f"{first}-{reader.line_num}"
            yield f"{source}:{location}", values


def bookings(stream, source="stdin"):
    rows = located_rows(stream, source)
    try:
        location, names = next(rows)
    except StopIteration:
        raise CalendarError(f"{source}: missing header") from None
    idx = {name: i for i, name in enumerate(names)}
    if len(idx) != len(names) or any(not n.strip() for n in names):
        raise CalendarError(f"{location}: duplicate or blank header name")
    if {"resource", "start", "end"}.difference(idx):
        raise CalendarError(f"{location}: expected resource, start and end columns")
    for location, fields in rows:
        if len(fields) != len(names):
            raise CalendarError(f"{location}: expected {len(names)} fields, found {len(fields)}")
        name = fields[idx["resource"]].strip()
        if not name or not name.isprintable():
            raise CalendarError(f"{location}: expected a nonblank printable resource name")
        try:
            block = Span(minute(fields[idx["start"]].strip()), minute(fields[idx["end"]].strip()))
        except ValueError as exc:
            raise CalendarError(f"{location}: {exc}") from exc
        status = fields[idx["status"]].strip().lower() if "status" in idx else "busy"
        status = status or "busy"
        if status not in ("busy", "tentative", "free", "cancelled"):
            raise CalendarError(f"{location}: unrecognized booking status")
        yield Booking(name, block, status)


class SelectionError(ValueError):
    pass


def select_bookings(entries, names):
    """Validate the entire selection, including names found only in later files."""
    wanted = set(names)
    missing = wanted.difference(b.resource for b in entries)
    if missing:
        raise SelectionError(f"unknown resource: {min(missing)!r}")
    return [b for b in entries if not wanted or b.resource in wanted]
