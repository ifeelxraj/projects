"""Generate candidate meetings from sorted disjoint free blocks."""

from .time import Span


def candidates(gaps, duration, step, anchor=0):
    if min(duration, step) <= 0:
        raise ValueError("duration and step must be positive")
    for gap in gaps:
        first = gap.start + (anchor - gap.start) % step
        for start in range(first, gap.end - duration + 1, step):
            yield Span(start, start + duration)
