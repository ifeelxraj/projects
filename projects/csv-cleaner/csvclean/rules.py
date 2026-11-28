"""Bind column names to checks once, before streaming data rows."""

from dataclasses import dataclass

from .layout import OptionError


@dataclass(frozen=True)
class Rules:
    required: tuple = ()

    def bind(self, header):
        positions = {name: i for i, name in enumerate(header)}
        checks = []
        for name in self.required:
            if name not in positions:
                raise OptionError(f"unknown required column: {name!r}")
            checks.append((positions[name], name, "must not be blank", lambda v: bool(v.strip())))
        return checks


def apply_checks(row, checks):
    for i, name, message, accepts in checks:
        if not accepts(row.fields[i]):
            raise row.problem(f"column {name!r} {message}")
