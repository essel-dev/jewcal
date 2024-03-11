"""Jewish dates with shabbos / yom tov details for Diaspora."""

from dataclasses import dataclass
from datetime import date
from typing import Any, Optional
from warnings import warn

from .constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Months
from .utils.calculations import (absdate_to_jewish, gregorian_to_absdate,
                                 weekday_from_absdate)


@dataclass
class JewCal:  # pylint: disable=too-many-instance-attributes
    """Jewish date with shabbos / yom tov details."""

    year: int
    """The year in the Jewish calendar."""

    month: int
    """The month in the Jewish calendar."""

    day: int
    """The day of the Jewish month."""

    gregorian_date: date
    """The date in the Gregorian calendar."""

    shabbos: Optional[str] = None
    """Is it (Erev) Shabbos."""

    yomtov: Optional[str] = None
    """Is it (Erev) Yom Tov."""

    category: Optional[str] = None
    """The category (Candles or Havdalah)."""

    diaspora: Optional[bool] = True
    """Is the schedule for Diaspora or Israel."""

    def __init__(self, gregorian_date: date, diaspora: bool = True) -> None:
        """Create a new Jewish date.

        The Jewish date contains optional details:
            - Shabbos or Yom Tov
            - category (Candles or Havdalah).

        If the first day of Yom Tov starts on Shabbos, the category is set
        to Candles instead of Havdalah.

        Args:
            gregorian_date: The Gregorian date.
            diaspora: True if outside of Israel, False if in Israel.
        """
        # jewish date
        absdate = gregorian_to_absdate(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        )
        self.year, self.month, self.day = absdate_to_jewish(absdate)

        # gregorian date
        self.gregorian_date = gregorian_date

        # diaspora
        self.diaspora = diaspora

        # shabbos
        weekday: int = weekday_from_absdate(absdate)
        if weekday in SHABBOS:
            event = SHABBOS[weekday]
            self.shabbos = event.title
            self.category = event.category

        # yom tov
        holidays = YOMTOV if self.diaspora else YOMTOV_ISRAEL
        if self.month in holidays and self.day in holidays[self.month]:
            event = holidays[self.month][self.day]
            self.yomtov = event.title
            if event.category:
                # don't overwrite category if chol hamoed is on shabbos
                self.category = event.category

    def __str__(self) -> str:
        """Jewish date as a string.

        Returns:
            The Jewish date.
        """
        return f'{self.day} {Months(self.month).name.capitalize()} {self.year}'


class Jewcal(JewCal):  # pylint: disable=too-few-public-methods
    """Deprecated class Jewcal has been renamed to JewCal.

    This class will be removed in a future release.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Return the new class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        warn('Class Jewcal is deprecated and renamed to JewCal')
