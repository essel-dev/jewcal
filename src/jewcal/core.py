"""Jewish Calendar."""

# https://stackoverflow.com/a/67483317
# Show return type in Sphinx without its full path
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

from .models.day import Day


@dataclass(slots=True)
class JewCal:
    """The Jewish Calendar.

    Calendars are cached when they are created. This optimization is
    noticeable when creating a large number of Jewish dates in a single
    run. In that scenario it is preferable to (re)set the
    current :py:meth:`date` on an existing JewCal-instance rather than
    creating new ones.

    .. see helpers.calendars
    """

    day: Day
    """The current day in the Jewish calendar."""

    _diaspora: bool = field(repr=False)
    """Is the calendar for Diaspora."""

    def __init__(
        self,
        gregorian: Optional[date] = None,
        diaspora: bool = True
    ) -> None:
        """Initialize a Jewish calendar.

        Args:
            gregorian: The Gregorian date. Default is today.
            diaspora: True if outside of Israel, False if in Israel.
        """
        self._diaspora = diaspora
        self.date(gregorian if gregorian is not None else date.today())

    def __str__(self) -> str:
        """Get the current calendar day as a readable string.

        Returns:
            The calendar day.
        """
        return str(self.day)

    def date(self, gregorian: date) -> None:
        """Set the current date.

        Args:
            gregorian: The Gregorian date.
        """
        self.day = Day(gregorian, self._diaspora)

    def days(self, days: int) -> list[Day]:
        """Get the next or past day(s).

        Args:
            days: The number of days to get.

        Returns:
            A list of days.

        Raises:
            TypeError: If `days` is an unsupported type.
            ValueError: If `days` is zero.
        """
        if not isinstance(days, int):
            raise TypeError(f'unsupported type {days.__class__.__name__}')

        if days == 0:
            raise ValueError('days must be positive or negative')

        selected_days = []

        if days > 0:  # next day(s)
            selected_days = self._select_days(
                quantity=days,
                start=1,
                stop=days + 1
            )

        if days < 0:  # past day(s)
            selected_days = self._select_days(
                quantity=days,
                start=0,
                stop=abs(days)
            )

        return selected_days

    def current_week(self) -> list[Day]:
        """Get the current week.

        Returns:
            A list of 7 days with Sunday as the first day of the week.
        """
        weekday = self.day.date.weekday

        return self._select_days(
            quantity=0,
            start=0 - weekday,
            stop=7 - weekday
        )

    def weeks(self, weeks: int) -> list[Day]:
        """Get the next or past week(s).

        Args:
            weeks: The number of weeks to get.

        Returns:
            Weeks as a list of days. The first day is Sunday.

        Raises:
            TypeError: If `weeks` is an unsupported type.
            ValueError: If `weeks` is zero.
        """
        if not isinstance(weeks, int):
            raise TypeError(f'unsupported type {weeks.__class__.__name__}')

        if weeks == 0:
            raise ValueError('weeks must be positive or negative')

        selected_days = []
        weekday = self.day.date.weekday

        if weeks > 0:  # next week(s)
            selected_days = self._select_days(
                quantity=weeks,
                start=7 - weekday,
                stop=7 - weekday + weeks * 7
            )

        if weeks < 0:  # past week(s)
            weeks = abs(weeks)

            selected_days = self._select_days(
                quantity=-(weekday + 7 * weeks),
                start=0,
                stop=7 * weeks
            )

        return selected_days

    def _select_days(self, quantity: int, start: int, stop: int) -> list[Day]:
        """Get a list of days.

        Possible options:
            - current week
            - next day(s) / week(s)
            - past day(s) / week(s)

        Args:
            quantity: The amount of days to get.
            start: The value of the start parameter used in `range`.
            stop: The value of the stop parameter used in `range`.

        Returns:
            A list of days.
        """
        gregorian = self.day.date.gregorian

        selected_days = []
        diaspora = self._diaspora

        if quantity == 0:  # current week
            selected_days = [
                Day(gregorian + timedelta(days=i), diaspora=diaspora)
                for i in range(start, stop)
            ]

        if quantity > 0:  # next day(s) / week(s)
            selected_days = [
                Day(gregorian + timedelta(days=i), diaspora=diaspora)
                for i in range(start, stop)
            ]

        if quantity < 0:  # past day(s) / week(s)
            start_date = gregorian - timedelta(days=abs(quantity))

            selected_days = [
                Day(start_date + timedelta(days=i), diaspora=diaspora)
                for i in range(start, stop)
            ]

        return selected_days
