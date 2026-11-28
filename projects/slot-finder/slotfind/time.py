"""Minute precision in one local day. No dates, time zones or implicit rollover."""

from dataclasses import dataclass
import re

DAY = 24 * 60


def minute(text):
    if not re.fullmatch(r"[0-9]{2}:[0-9]{2}", text):
        raise ValueError(f"expected HH:MM, got {text!r}")
    hour, part = map(int, text.split(":"))
    if hour == 24 and part == 0:
        return DAY
    if hour >= 24 or part >= 60:
        raise ValueError(f"time outside day: {text!r}")
    return hour * 60 + part


def clock(value):
    if not 0 <= value <= DAY:
        raise ValueError("minutes outside day")
    return f"{value // 60:02d}:{value % 60:02d}"


@dataclass(frozen=True, order=True)
class Span:
    start: int
    end: int

    def __post_init__(self):
        if not 0 <= self.start < self.end <= DAY:
            raise ValueError("interval must start before its end within one day")

    @property
    def minutes(self):
        return self.end - self.start

    def padded(self, before=0, after=0):
        if min(before, after) < 0:
            raise ValueError("padding cannot be negative")
        return Span(max(0, self.start - before), min(DAY, self.end + after))

    def intersect(self, other):
        lo, hi = max(self.start, other.start), min(self.end, other.end)
        return Span(lo, hi) if lo < hi else None

    def contains(self, other):
        return self.start <= other.start and other.end <= self.end

    def __str__(self):
        return f"{clock(self.start)}-{clock(self.end)}"


def span(text):
    pieces = text.split("-")
    if len(pieces) != 2:
        raise ValueError(f"expected HH:MM-HH:MM, got {text!r}")
    return Span(*(minute(part) for part in pieces))
