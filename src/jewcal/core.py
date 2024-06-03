"""Usage examples.

**Diaspora:**

>>> jewcal = JewCal(date.today())  # today's date

>>> jewcal = JewCal(date(2022, 4, 17))  # specific date
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
JewCal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17),
shabbos=None, yomtov='Pesach 2', category='Havdalah', diaspora=True)


**Israel:**

>>> jewcal = JewCal(date.today(), diaspora=False)  # today's date

>>> jewcal = JewCal(date(2022, 4, 17), diaspora=False)  # specific date
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
JewCal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17),
shabbos=None, yomtov='Chol HaMoed 1 (Pesach 2)', category=None, diaspora=False)
"""

from dataclasses import dataclass
from datetime import date

from .constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Category, Months
from .utils.calculations import (
    absdate_to_jewish,
    gregorian_to_absdate,
    weekday_from_absdate,
)


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

    shabbos: str | None = None
    """Is it (Erev) Shabbos."""

    yomtov: str | None = None
    """Is it (Erev) Yom Tov."""

    category: str | None = None
    """The category (Candles or Havdalah)."""

    diaspora: bool | None = True
    """Is the schedule for Diaspora or Israel."""

    def __init__(self, gregorian_date: date, diaspora: bool = True) -> None:
        """Create a new Jewish date.

        The Jewish date contains optional details:
            - Shabbos or Yom Tov
            - category (Candles or Havdalah).

        If Shabbos / Yom Tov has Candles / Havdalah, Candles has priority. The category
        is set to Candles instead of Havdalah.

        Args:
            gregorian_date: The Gregorian date.
            diaspora: True if outside of Israel, False if in Israel.
        """
        # jewish date
        absdate = gregorian_to_absdate(
            gregorian_date.year, gregorian_date.month, gregorian_date.day
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

            # don't overwrite category `None` if Chol HaMoed is on Shabbos
            if event.category:
                if not self.category:
                    self.category = event.category
                elif self.category != event.category:
                    # if Shabbos / Yom Tov has Candles / Havdalah, Candles has priority
                    self.category = Category.CANDLES.value

    def __str__(self) -> str:
        """Jewish date as a string.

        Returns:
            The Jewish date.
        """
        return f'{self.day} {Months(self.month).name.capitalize()} {self.year}'
