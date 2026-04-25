"""durfmt — format timedeltas and numeric seconds as human-readable durations.

Public API:

* :func:`format_duration` — format like "1h 30m 12s" with custom unit set.
* :func:`format_clock`    — format like "01:30:12" or "1:30:12.345".
* :class:`DurFmtError`    — raised on invalid input (ValueError subclass).
"""

from __future__ import annotations

from ._core import (
    DurFmtError,
    format_clock,
    format_duration,
)

__all__ = [
    "DurFmtError",
    "format_clock",
    "format_duration",
]

__version__ = "0.1.0"
