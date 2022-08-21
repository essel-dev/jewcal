"""Jewish dates with Shabbos / holiday details for Diaspora."""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Union, cast

from .constants import HOLIDAYS, SHABBOS, Category, Months
from .utils.calculations import (
    absdate_to_jewish,
    weekday_from_absdate,
    gregorian_to_absdate
)


@dataclass
class Jewcal:
    """Jewish date with Shabbos / holiday details."""

    year: int
    month: int
    day: int
    shabbos: Optional[str] = None
    holiday: Optional[str] = None
    category: Optional[Category] = None

    def __init__(self, gregorian_date: date) -> None:
        """Create a new jewish date.

        The jewish date contains optional details:
            - Shabbos or holiday
            - category (candles or havdalah).

        If the first day of a holiday falls on Shabbos, it will set the
        category to candles instead of havdalah.

        Args:
            gregorian_date: The Gregorian date.
        """
        # date
        absdate = gregorian_to_absdate(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        )
        self.year, self.month, self.day = absdate_to_jewish(absdate)

        # Shabbos / holiday / category
        weekday: int = weekday_from_absdate(absdate)
        if weekday in SHABBOS:
            self.shabbos = cast(str, SHABBOS[weekday][0])
            self.category = cast(Category, SHABBOS[weekday][1])

        holiday_attributes: Optional[List[Union[str, Category]]] = None
        try:
            holiday_attributes = HOLIDAYS[self.month][self.day]
        except KeyError:
            pass

        if holiday_attributes:
            self.holiday = cast(str, holiday_attributes[0])
            self.category = cast(Category, holiday_attributes[1])

    def __str__(self) -> str:
        """Jewish date as a string.

        Returns:
            The jewish date.
        """
        return f'{self.day} {Months(self.month).name.capitalize()} {self.year}'
