"""A prepared schedule shared by availability queries and reports."""

from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from .availability import available_across, union
from .calendar import select_bookings
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
