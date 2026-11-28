"""Read logical records while retaining their physical source locations."""

import csv
from dataclasses import dataclass, field


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


def records(stream, delimiter=",", *, skip_blank=False):
    reader = csv.reader(stream, delimiter=delimiter, strict=True)
    while True:
        first = reader.line_num + 1
        try:
            values = next(reader)
        except StopIteration:
            return
        except csv.Error as exc:
            raise Problem(str(exc), first, max(first, reader.line_num)) from exc
        if skip_blank and not values:
            continue
        yield Record(first, reader.line_num, tuple(values))


def read_header(rows, *, trim=False):
    try:
        row = next(rows)
    except StopIteration:
        raise Problem("missing header", 1, 1) from None
    if not row.fields:
        raise row.problem("empty header record")
    names = tuple(name.strip() for name in row.fields) if trim else row.fields
    seen = set()
    for index, name in enumerate(names, 1):
        if not name.strip():
            raise row.problem(f"blank header at column {index}")
        if name in seen:
            raise row.problem(f"duplicate header at column {index}: {name!r}")
        seen.add(name)
    return names


def check_width(row, header):
    if len(row.fields) != len(header):
        raise row.problem(f"expected {len(header)} fields, found {len(row.fields)}")


@dataclass
class Report:
    header: tuple = ()
    examined: int = 0
    problems: list = field(default_factory=list)
    stopped: bool = False


def audit(stream, delimiter=",", *, skip_blank=False, max_errors=1, trim_header=False):
    if max_errors < 1:
        raise ValueError("max_errors must be positive")
    result = Report()
    try:
        rows = records(stream, delimiter, skip_blank=skip_blank)
        result.header = read_header(rows, trim=trim_header)
        for row in rows:
            result.examined += 1
            try:
                check_width(row, result.header)
            except Problem as exc:
                result.problems.append(exc)
                if len(result.problems) >= max_errors:
                    result.stopped = True
                    break
    except Problem as exc:  # Bad quoting or an unusable header cannot be recovered.
        result.problems.append(exc)
        result.stopped = True
    return result


def validate(stream, delimiter=",", *, skip_blank=False):
    report = audit(stream, delimiter, skip_blank=skip_blank)
    if report.problems:
        raise report.problems[0]
    return report.header, report.examined
