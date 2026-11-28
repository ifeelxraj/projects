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
