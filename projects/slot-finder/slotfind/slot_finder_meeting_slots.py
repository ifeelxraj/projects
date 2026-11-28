"""Generate candidate meetings from sorted disjoint free blocks."""

from .slot_finder_time_ranges import Span


def candidates(gaps, duration, step, anchor=0):
    if any(type(n) is not int for n in (duration, step, anchor)):
        raise ValueError("duration, step and anchor must use whole minutes")
    if min(duration, step) <= 0:
        raise ValueError("duration and step must be positive")
    for gap in gaps:
        first = gap.start + (anchor - gap.start) % step
        for start in range(first, gap.end - duration + 1, step):
            yield Span(start, start + duration)


def non_overlapping(chronological):
    """Earliest finish is optimal for these equal-length meeting candidates."""
    next_start = 0
    for block in chronological:
        if block.start >= next_start:
            yield block
            next_start = block.end
