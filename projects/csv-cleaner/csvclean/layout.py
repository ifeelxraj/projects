"""Compile named output columns once, before writing the header."""

from dataclasses import dataclass


class OptionError(ValueError):
    """The requested transformation cannot apply to this table."""


@dataclass(frozen=True)
class Layout:
    names: tuple
    indices: tuple

    def select(self, fields):
        return tuple(fields[i] for i in self.indices)


def compile_layout(header, *, keep=()):
    positions = {name: i for i, name in enumerate(header)}
    names = tuple(keep) if keep else header
    if len(set(names)) != len(names):
        raise OptionError("repeated column selection")
    for name in names:
        if name not in positions:
            raise OptionError(f"unknown column: {name!r}")
    return Layout(names, tuple(positions[name] for name in names))
