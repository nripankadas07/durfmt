"""durfmt — format timedeltas and seconds as human-readable durations."""
from __future__ import annotations

import math
from datetime import timedelta
from typing import Union

__all__ = ["DurFmtError", "format_clock", "format_duration"]
__version__ = "0.1.0"

_UNITS = (
    ("w", "week", "weeks", 604800.0),
    ("d", "day", "days", 86400.0),
    ("h", "hour", "hours", 3600.0),
    ("m", "minute", "minutes", 60.0),
    ("s", "second", "seconds", 1.0),
)


class DurFmtError(ValueError):
    """Raised on invalid input."""


def _coerce_seconds(value: object) -> float:
    if isinstance(value, timedelta):
        return value.total_seconds()
    if isinstance(value, bool):
        raise DurFmtError("value must be a number or timedelta, not bool")
    if isinstance(value, (int, float)):
        seconds = float(value)
        if not math.isfinite(seconds):
            raise DurFmtError("value must be finite")
        return seconds
    raise DurFmtError(
        f"value must be int, float, or timedelta; got {type(value).__name__}"
    )


def format_duration(
    value: Union[int, float, timedelta],
    *,
    units: str = "short",
    sep: str = " ",
    precision: int = 3,
) -> str:
    """Format value as "1h 30m 12s" (short) or "1 hour 30 minutes 12 seconds" (long)."""
    if units not in ("short", "long"):
        raise DurFmtError(f"units must be 'short' or 'long', got {units!r}")
    if not isinstance(precision, int) or precision < 0:
        raise DurFmtError("precision must be a non-negative int")
    if not isinstance(sep, str):
        raise DurFmtError("sep must be a string")
    seconds = _coerce_seconds(value)
    sign = ""
    if seconds < 0:
        sign = "-"
        seconds = -seconds
    parts = []
    fractional = 0.0
    for symbol, sing, plur, secs_per in _UNITS[:-1]:
        if seconds >= secs_per:
            n = int(seconds // secs_per)
            seconds -= n * secs_per
            label = (sing if n == 1 else plur) if units == "long" else symbol
            parts.append(f"{n} {label}" if units == "long" else f"{n}{label}")
    # Last unit (seconds) - include fractional
    if seconds > 0 or not parts:
        if precision > 0 and seconds != int(seconds):
            label = "second" if units == "long" and seconds == 1 else ("seconds" if units == "long" else "s")
            text = f"{seconds:.{precision}f}".rstrip("0").rstrip(".")
            parts.append(f"{text} {label}" if units == "long" else f"{text}{label}")
        else:
            n = int(seconds)
            label = (("second" if n == 1 else "seconds") if units == "long" else "s")
            parts.append(f"{n} {label}" if units == "long" else f"{n}{label}")
    return sign + sep.join(parts)


def format_clock(
    value: Union[int, float, timedelta],
    *,
    hours_required: bool = False,
) -> str:
    """Format value as HH:MM:SS or MM:SS clock string."""
    seconds = _coerce_seconds(value)
    sign = ""
    if seconds < 0:
        sign = "-"
        seconds = -seconds
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds - h * 3600 - m * 60
    if h > 0 or hours_required:
        if s != int(s):
            return f"{sign}{h:02d}:{m:02d}:{s:06.3f}"
        return f"{sign}{h:02d}:{m:02d}:{int(s):02d}"
    if s != int(s):
        return f"{sign}{m:02d}:{s:06.3f}"
    return f"{sign}{m:02d}:{int(s):02d}"
