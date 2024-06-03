"""Usage examples.

**Diaspora:**

>>> jewcal = JewCal(date.today())  # today's date

>>> jewcal = JewCal(date(2022, 4, 17))  # specific date
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
JewCal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17),
shabbos=None, yomtov='Pesach 2', category='Havdalah', is_erev=False,
is_issur_melacha=True, diaspora=True)


**Israel:**

>>> jewcal = JewCal(date.today(), diaspora=False)  # today's date

>>> jewcal = JewCal(date(2022, 4, 17), diaspora=False)  # specific date
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
JewCal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17),
shabbos=None, yomtov='Chol HaMoed 1 (Pesach 2)', category=None, is_erev=False,
is_issur_melacha=False, diaspora=False)
"""

from dataclasses import dataclass, field
from datetime import date

from .constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Category, Month
from .utils.calculations import (
    absdate_to_jewish,
    gregorian_to_absdate,
    is_jewish_leap,
    weekday_from_absdate,
)


@dataclass
class JewCal:  # pylint: disable=too-many-instance-attributes
    """Convert Gregorian to Jewish dates for Diaspora and Israel.

    The `JewCal` object contains:
        - Shabbos and Yom Tov details
        - The category (`Candles` or `Havdalah`)
        - Is it Erev Shabbos or Yom Tov
        - Is it Issur Melacha
    """

    year: int
    """The year in the Jewish calendar."""

    month: int
    """The month in the Jewish year."""

    day: int
    """The day in the Jewish month."""

    _is_leap: bool = field(repr=False)
    """Is it a Jewish leap year."""

    gregorian_date: date
    """The date in the Gregorian calendar."""

    shabbos: str | None = None
    """(Erev) Shabbos definition."""

    yomtov: str | None = None
    """(Erev) Yom Tov definition."""

    category: str | None = None
    """The category (`Candles` or `Havdalah`).

    If Shabbos and Yom Tov has `Candles` and `Havdalah`, `Candles` has priority.
    """

    is_erev: bool = False
    """Is it Erev Shabbos or Yom Tov."""

    is_issur_melacha: bool = False
    """Is it Issur Melacha."""

    diaspora: bool = True
    """Is the schedule for Diaspora or Israel."""

    def __init__(self, gregorian_date: date, diaspora: bool = True) -> None:
        """Create a new Jewish date.

        Args:
            gregorian_date: The Gregorian date.
            diaspora: True if outside of Israel, False if in Israel.
        """
        # jewish date
        absdate = gregorian_to_absdate(
            gregorian_date.year, gregorian_date.month, gregorian_date.day
        )
        self.year, self.month, self.day = absdate_to_jewish(absdate)
        self._is_leap = is_jewish_leap(self.year)

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

        # erev
        self._erev()

        # issur melacha
        self._issur_melacha()

    def __str__(self) -> str:
        """Jewish date as a string.

        Returns:
            The Jewish date.
        """
        return (
            f'{self.day}'
            f' {Month.get(self.month, self._is_leap)}'  # Adar 1/2 in leap year
            f' {self.year}'
        )

    def _erev(self) -> None:
        is_erev_shabbos = self.shabbos and 'Erev' in self.shabbos

        is_erev_yom_tov = self.yomtov and any(
            [
                'Erev' in self.yomtov,
                'Hoshana Rabba' in self.yomtov,
                'Pesach 6' in self.yomtov,
            ]
        )

        if self.category == 'Candles' and any(
            [
                is_erev_shabbos and not self.yomtov,
                is_erev_shabbos and is_erev_yom_tov,
                is_erev_shabbos and self.yomtov and 'Chol HaMoed' in self.yomtov,
                not is_erev_shabbos and is_erev_yom_tov,
            ]
        ):
            self.is_erev = True

    def _issur_melacha(self) -> None:
        """Is it issur melacha."""
        self.is_issur_melacha = self.category is not None and not self.is_erev
