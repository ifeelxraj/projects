"""Bind column names to checks once, before streaming data rows."""

from dataclasses import dataclass
import re

from .layout import OptionError


@dataclass(frozen=True)
class Rules:
    required: tuple = ()
    integer: tuple = ()

    def bind(self, header):
        positions = {name: i for i, name in enumerate(header)}
        checks = []
        groups = [
            (self.required, "must not be blank", lambda v: bool(v.strip())),
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
