"""A prepared schedule shared by availability queries and reports."""

from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from .availability import available_across, union
from .calendar import select_bookings
from .slots import candidates, non_overlapping
from .time import Span


@dataclass(frozen=True)
class Blocker:
    resource: Optional[str]  # None means a manual block for everyone.
    interval: Span


@dataclass(frozen=True)
class Plan:
    windows: tuple
    resources: tuple
    blockers: tuple

    def explain(self, request):
        inside = any(window.contains(request) for window in self.windows)
        conflicts = []
        for blocker in self.blockers:
            overlap = request.intersect(blocker.interval)
            if overlap:
                conflicts.append({"resource": blocker.resource, "blocked": str(blocker.interval), "overlap": str(overlap)})
        return {"request": str(request), "inside_work": inside, "available": inside and not conflicts,
                "conflicts": conflicts}

    def capacity(self, duration, step, anchor=0):
        packed = non_overlapping(candidates(self.gaps, duration, step, anchor))
        return sum(1 for _ in packed)

    def summary(self):
        working = sum(w.minutes for w in self.windows)
        free = sum(g.minutes for g in self.gaps)
        return {"work_minutes": working, "busy_minutes": working - free, "free_minutes": free,
                "free_blocks": len(self.gaps), "longest_free_minutes": max((g.minutes for g in self.gaps), default=0)}

    @cached_property
    def gaps(self):
        return tuple(available_across(self.windows, (b.interval for b in self.blockers)))


def prepare(windows, manual, entries, *, names=(), before=0, after=0, ignore_tentative=False):
    selected = select_bookings(entries, names)
    resources = tuple(sorted({b.resource for b in selected}))
    blockers = [Blocker(None, period.padded(before, after)) for period in manual]
    blockers.extend(Blocker(b.resource, b.interval.padded(before, after)) for b in selected
                    if b.blocks(ignore_tentative=ignore_tentative))
    return Plan(tuple(union(windows)), resources, tuple(blockers))
