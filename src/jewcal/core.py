"""Jewish dates with shabbos / yomtov details for Diaspora."""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Union, cast

from .constants import YOMTOV, SHABBOS, Category, Months
from .utils.calculations import (
    absdate_to_jewish,
    weekday_from_absdate,
    gregorian_to_absdate
)


@dataclass
class Jewcal:
    """Jewish date with shabbos / yomtov details."""

    year: int
    month: int
    day: int
    shabbos: Optional[str] = None
    yomtov: Optional[str] = None
    category: Optional[Category] = None

    def __init__(self, gregorian_date: date) -> None:
        """Create a new jewish date.

        The jewish date contains optional details:
            - shabbos or yomtov
            - category (candles or havdalah).

        If the first day of a yomtov falls on shabbos, the category is set to
        candles instead of havdalah.

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

        # shabbos / yomtov / category
        weekday: int = weekday_from_absdate(absdate)
        if weekday in SHABBOS:
            self.shabbos = cast(str, SHABBOS[weekday][0])
            self.category = cast(Category, SHABBOS[weekday][1])

        yomtov_attributes: Optional[List[Union[str, Category]]] = None
        try:
            yomtov_attributes = YOMTOV[self.month][self.day]
        except KeyError:
            pass

        if yomtov_attributes:
            self.yomtov = cast(str, yomtov_attributes[0])
            self.category = cast(Category, yomtov_attributes[1])

    def __str__(self) -> str:
        """Jewish date as a string.

        Returns:
            The jewish date.
        """
        return f'{self.day} {Months(self.month).name.capitalize()} {self.year}'
