from .time import Span


def union(intervals):
    """Return sorted disjoint spans; adjacent spans leave no available minute."""
    merged = []
    for item in sorted(intervals):
        if merged and item.start <= merged[-1].end:
            last = merged[-1]
            merged[-1] = Span(last.start, max(last.end, item.end))
        else:
            merged.append(item)
    return merged


def available(window, busy):
    """Subtract the union of in-window bookings from the work window."""
    gaps = []
    cursor = window.start
    for stop in union(part for item in busy if (part := window.intersect(item))):
        if cursor < stop.start:
            gaps.append(Span(cursor, stop.start))
        cursor = stop.end
    if cursor < window.end:
        gaps.append(Span(cursor, window.end))
    return gaps
