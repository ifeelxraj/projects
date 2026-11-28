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


def compile_layout(header, *, keep=(), drop=()):
    positions = {name: i for i, name in enumerate(header)}
    if keep and drop:
        raise OptionError("choose either --keep or --drop")
    omitted = set(drop)
    if len(omitted) != len(drop) or omitted.difference(positions):
        raise OptionError("unknown or repeated column in --drop")
    names = tuple(keep) if keep else tuple(n for n in header if n not in omitted)
    if not names:
        raise OptionError("cannot drop all columns")
    if len(set(names)) != len(names):
        raise OptionError("repeated column selection")
    for name in names:
        if name not in positions:
            raise OptionError(f"unknown column: {name!r}")
    return Layout(names, tuple(positions[name] for name in names))
