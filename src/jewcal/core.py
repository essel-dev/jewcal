"""Jewish dates with shabbos / yom tov details for Diaspora."""

from dataclasses import dataclass
from datetime import date
from typing import Optional

from .constants import YOMTOV, SHABBOS, Category, Months
from .utils.calculations import (
    absdate_to_jewish,
    weekday_from_absdate,
    gregorian_to_absdate
)


@dataclass
class Jewcal:
    """Jewish date with shabbos / yom tov details."""

    year: int
    month: int
    day: int
    shabbos: Optional[str] = None
    yomtov: Optional[str] = None
    category: Optional[Category] = None

    def __init__(self, gregorian_date: date) -> None:
        """Create a new Jewish date.

        The Jewish date contains optional details:
            - shabbos or yom tov
            - category (candles or havdalah).

        If the first day of a yom tov starts on shabbos, the category is set
        to candles instead of havdalah.

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

        # shabbos
        weekday: int = weekday_from_absdate(absdate)
        if weekday in SHABBOS:
            event = SHABBOS[weekday]
            self.shabbos = event.title
            self.category = event.category

        # yom tov
        try:
            event = YOMTOV[self.month][self.day]
            self.yomtov = event.title
            self.category = event.category
        except KeyError:
            pass

    def __str__(self) -> str:
        """Jewish date as a string.

        Returns:
            The Jewish date.
        """
        return f'{self.day} {Months(self.month).name.capitalize()} {self.year}'
