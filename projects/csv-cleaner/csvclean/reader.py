"""Read logical records while retaining their physical source locations."""

import csv
from dataclasses import dataclass


class Problem(ValueError):
    def __init__(self, message, first, last):
        self.message, self.first, self.last = message, first, last
        location = f"line {first}" if first == last else f"lines {first}-{last}"
        super().__init__(f"{location}: {message}")


@dataclass(frozen=True)
class Record:
    first: int
    last: int
    fields: tuple

    def problem(self, message):
        return Problem(message, self.first, self.last)


def records(stream, delimiter=","):
    reader = csv.reader(stream, delimiter=delimiter, strict=True)
    while True:
        first = reader.line_num + 1
        try:
            values = next(reader)
        except StopIteration:
            return
        except csv.Error as exc:
            raise Problem(str(exc), first, max(first, reader.line_num)) from exc
        yield Record(first, reader.line_num, tuple(values))


def read_header(rows):
    try:
        row = next(rows)
    except StopIteration:
        raise Problem("missing header", 1, 1) from None
    if not row.fields:
        raise row.problem("empty header record")
    seen = set()
    for index, name in enumerate(row.fields, 1):
        if not name.strip():
            raise row.problem(f"blank header at column {index}")
        if name in seen:
            raise row.problem(f"duplicate header at column {index}: {name!r}")
        seen.add(name)
    return row.fields
