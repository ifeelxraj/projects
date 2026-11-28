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
