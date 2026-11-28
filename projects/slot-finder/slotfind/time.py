"""Minute precision in one local day. No dates, time zones or implicit rollover."""

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
