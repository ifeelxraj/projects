"""Bind column names to checks once, before streaming data rows."""

from dataclasses import dataclass
from datetime import date
import re

from .csv_cleaner_columns import OptionError


def iso_date(value):
    if not value:
        return True
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


@dataclass(frozen=True)
class Rules:
    columns: tuple = ()
    required: tuple = ()
    integer: tuple = ()
    date: tuple = ()
    decimal: tuple = ()

    def bind(self, header):
        positions = {name: i for i, name in enumerate(header)}
        numeric = set(self.integer).union(self.decimal)
        conflicting = numeric.intersection(self.date)
        if conflicting:
            raise OptionError(f"column cannot be both numeric and a date: {min(conflicting)!r}")
        checks = []
        groups = [
            (self.required, "must not be blank", lambda v: bool(v.strip())),
            (self.decimal, "must be a plain decimal",
             lambda v: not v or re.fullmatch(r"[+-]?[0-9]+(?:\.[0-9]+)?", v)),
            (self.date, "must be a YYYY-MM-DD date", iso_date),
            (self.integer, "must be an integer", lambda v: not v or re.fullmatch(r"[+-]?[0-9]+", v)),
        ]
        for names, message, accepts in groups:
            for name in dict.fromkeys(names):
                if name not in positions:
                    raise OptionError(f"unknown rule column: {name!r}")
                checks.append((positions[name], name, message, accepts))
        return checks


def apply_checks(row, checks):
    for i, name, message, accepts in checks:
        if not accepts(row.fields[i]):
            raise row.problem(f"column {name!r} {message}")
