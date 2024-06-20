"""Datetime utilities to enable dependency injection.

Built-in modules written in C cannot be mocked when unittesting.

https://hakibenita.com/python-dependency-injection.
"""

from datetime import date, datetime, timezone


def datetime_now() -> datetime:
    """Get the current date and time.

    Returns:
        The current date and time in UTC.
    """
    return datetime.now(tz=timezone.utc)


def date_today() -> date:
    """Get the current date.

    Returns:
        The current date.
    """
    return datetime.now(tz=timezone.utc).date()
