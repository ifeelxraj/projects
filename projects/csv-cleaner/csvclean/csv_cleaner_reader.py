"""Read logical records while retaining their physical source locations."""

import csv
from dataclasses import dataclass, field


from .csv_cleaner_columns import OptionError, compile_layout
from .csv_cleaner_value_rules import Rules, apply_checks


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


def read_header(rows, *, trim=False, expected=()):
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
    if expected and names != expected:
        raise row.problem("header names or order differ from schema columns")
    return names


def check_width(row, header):
    if len(row.fields) != len(header):
        raise row.problem(f"expected {len(header)} fields, found {len(row.fields)}")


class Table:
    """A single-pass table. Ordinary iteration yields checked records only."""

    def __init__(self, stream, delimiter=",", *, skip_blank=False, trim_header=False, rules=Rules(), order_by=(), strict_order=False):
        self.rows = records(stream, delimiter, skip_blank=skip_blank)
        self.header = read_header(self.rows, trim=trim_header, expected=rules.columns)
        self.checks = rules.bind(self.header)
        if strict_order and not order_by:
            raise OptionError("--strict-order requires --order-by")
        self.strict_order = strict_order
        self.key = compile_layout(self.header, keep=order_by) if order_by else None
        self.previous_key = None

    def check(self, row):
        check_width(row, self.header)
        apply_checks(row, self.checks)
        if self.key:
            previous, current = self.previous_key, self.key.select(row.fields)
            self.previous_key = current
            if self.strict_order and previous == current:
                raise row.problem("duplicate ordered key")
            if previous is not None and current < previous:
                raise row.problem("sort key decreases relative to the preceding valid row")

    def __iter__(self):
        for row in self.rows:
            self.check(row)
            yield row


@dataclass
class Report:
    header: tuple = ()
    examined: int = 0
    problems: list = field(default_factory=list)
    stopped: bool = False

    def add(self, issue):
        # Raised exceptions own tracebacks, which can retain raw cells, streams
        # and the audit frame. A saved report needs only the diagnostic itself.
        self.problems.append(Problem(issue.message, issue.first, issue.last))


def audit(stream, delimiter=",", *, max_errors=1, **options):
    if max_errors < 1:
        raise ValueError("max_errors must be positive")
    result = Report()
    try:
        table = Table(stream, delimiter, **options)
        result.header = table.header
        for row in table.rows:
            result.examined += 1
            try:
                table.check(row)
            except Problem as exc:
                result.add(exc)
                if len(result.problems) >= max_errors:
                    result.stopped = True
                    break
    except Problem as exc:  # Bad quoting or an unusable header cannot be recovered.
        result.add(exc)
        result.stopped = True
    return result


def validate(stream, delimiter=",", *, skip_blank=False):
    report = audit(stream, delimiter, skip_blank=skip_blank)
    if report.problems:
        raise report.problems[0]
    return report.header, report.examined
