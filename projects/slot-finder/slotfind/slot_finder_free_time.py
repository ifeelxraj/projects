from .slot_finder_time_ranges import Span


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


def available_across(windows, busy):
    """Subtract two unions with forward-only cursors, including split shifts."""
    stops = union(busy)
    gaps = []
    i = 0
    for window in union(windows):
        cursor = window.start
        while i < len(stops) and stops[i].start < window.end:
            stop = stops[i]
            if cursor < stop.start:
                gaps.append(Span(cursor, stop.start))
            cursor = max(cursor, stop.end)
            if stop.end > window.end:
                break  # This booking may extend into the next work window.
            i += 1
        if cursor < window.end:
            gaps.append(Span(cursor, window.end))
    return gaps


def available(window, busy):
    return available_across([window], busy)
