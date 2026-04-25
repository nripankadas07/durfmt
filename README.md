# durfmt

Zero-dependency Python library for formatting timedeltas and numeric seconds as human-readable durations like `"1h 30m 12s"` or `"01:30:12"`.

## Install

```bash
pip install durfmt
```

Requires Python 3.10+. No runtime dependencies.

## Quick example

```python
from datetime import timedelta
from durfmt import format_duration, format_clock

format_duration(5400)                           # "1h 30m"
format_duration(timedelta(seconds=5412.345))    # "1h 30m 12.345s"
format_duration(60, units="long")               # "1 minute"
format_duration(3661, units=("h","m","s"), sep=":")  # "1:1:1"
format_duration(0)                              # "0s"

format_clock(5400)                              # "01:30:00"
format_clock(5412.345)                          # "01:30:12.345"
format_clock(7325, hours_required=True)         # "02:02:05"
format_clock(timedelta(hours=25, minutes=30))   # "25:30:00"
```

## Quality

- **117 tests, 100% line coverage**
- Zero runtime dependencies
- Strict type hints throughout

## API

### `format_duration(value, *, units="short", sep=" ", precision=3) -> str`
Format a `timedelta` or numeric seconds value as `"1h 30m 12s"` (short) or `"1 hour 30 minutes 12 seconds"` (long).

### `format_clock(value, *, hours_required=False) -> str`
Format as `"HH:MM:SS"` or `"MM:SS"` clock string. Fractional seconds preserved.

### `DurFmtError`
Subclass of `ValueError`.

## Running tests

```bash
pip install -e ".[dev]"
pytest                           # 117 tests
pytest --cov=durfmt              # 100% line coverage
```

## License

MIT
