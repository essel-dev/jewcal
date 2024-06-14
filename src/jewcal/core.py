"""Usage examples.

**Diaspora:**

>>> jewcal = JewCal()  # today's date

>>> jewcal = JewCal(date(2022, 4, 17))  # specific date
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
JewCal(jewish_date=JewishDate(year=5782, month=1, day=16,
gregorian_date=datetime.date(2022, 4, 17)),
shabbos=None, yomtov='Pesach 2', category='Havdalah', is_erev=False,
is_issur_melacha=True, diaspora=True)


**Israel:**

>>> jewcal = JewCal(diaspora=False)  # today's date

>>> jewcal = JewCal(date(2022, 4, 17), diaspora=False)  # specific date
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
JewCal(jewish_date=JewishDate(year=5782, month=1, day=16,
gregorian_date=datetime.date(2022, 4, 17)),
shabbos=None, yomtov='Chol HaMoed 1 (Pesach 2)', category=None, is_erev=False,
is_issur_melacha=False, diaspora=False)
"""

from dataclasses import InitVar, dataclass, field
from datetime import date, datetime, timezone
from warnings import warn

from jewcal.models.jewish_date import JewishDate

from .constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Category
from .utils.calculations import (
    absdate_to_jewish,
    gregorian_to_absdate,
    is_jewish_leap,
    weekday_from_absdate,
)


@dataclass
class JewCal:
    """Convert Gregorian to Jewish dates for Diaspora and Israel.

    The `JewCal` object contains:
        - Shabbos and Yom Tov details
        - The category (`Candles` or `Havdalah`)
        - Is it Erev Shabbos or Yom Tov
        - Is it Issur Melacha
    """

    jewish_date: JewishDate = field(init=False)
    """The date in the Jewish calendar."""

    _gregorian: InitVar[date] = field(default=datetime.now(tz=timezone.utc).date())

    shabbos: str | None = field(init=False, default=None)
    """(Erev) Shabbos definition."""

    yomtov: str | None = field(init=False, default=None)
    """(Erev) Yom Tov definition."""

    category: str | None = field(init=False, default=None)
    """The category (`Candles` or `Havdalah`).

    If Shabbos and Yom Tov has `Candles` and `Havdalah`, `Candles` has priority.
    """

    is_erev: bool = field(init=False, default=False)
    """Is it Erev Shabbos or Yom Tov."""

    is_issur_melacha: bool = field(init=False, default=False)
    """Is it Issur Melacha."""

    diaspora: bool = field(default=True)
    """Is the schedule for Diaspora or Israel.

    True if outside of Israel, False if in Israel.
    """

    def __post_init__(self, gregorian: date) -> None:
        """Create a new Jewish date.

        Args:
            gregorian: The Gregorian date to convert from.
        """
        absdate = gregorian_to_absdate(gregorian.year, gregorian.month, gregorian.day)
        year, month, day = absdate_to_jewish(absdate)
        is_leap = is_jewish_leap(year)
        self.jewish_date = JewishDate(year, month, day, gregorian, is_leap)

        self._shabbos(absdate)
        self._yomtov()
        self._erev()
        self._issur_melacha()

    def __str__(self) -> str:
        """The Jewish date as a string.

        Returns:
            The Jewish date.
        """
        return str(self.jewish_date)

    @property
    def year(self) -> int:
        """Get the year in the Jewish calendar.

        .. deprecated:: 0.6.0 Use :py:attr:`jewish_date` ``.year``

        Returns:
            The year in the Jewish calendar.
        """
        warn('year is deprecated, use jewish_date.year', stacklevel=2)
        year: int = self.jewish_date.year
        return year

    @property
    def month(self) -> int:
        """Get the month in the Jewish year.

        .. deprecated:: 0.6.0 Use :py:attr:`jewish_date` ``.month``

        Returns:
            The month in the Jewish year.
        """
        warn('month is deprecated, use jewish_date.month', stacklevel=2)
        month: int = self.jewish_date.month
        return month

    @property
    def day(self) -> int:
        """Get the day in the Jewish month.

        .. deprecated:: 0.6.0 Use :py:attr:`jewish_date` ``.day``

        Returns:
            The day in the Jewish month.
        """
        warn('day is deprecated, use jewish_date.day', stacklevel=2)
        day: int = self.jewish_date.day
        return day

    @property
    def gregorian_date(self) -> date:
        """Get the Gregorian date.

        .. deprecated:: 0.6.0 Use :py:attr:`jewish_date` ``.gregorian_date``

        Returns:
            The date in the Gregorian calendar.
        """
        warn(
            'gregorian_date is deprecated, use jewish_date.gregorian_date',
            stacklevel=2,
        )
        gregorian_date: date = self.jewish_date.gregorian_date
        return gregorian_date

    def _shabbos(self, absdate: int) -> None:
        weekday: int = weekday_from_absdate(absdate)
        if weekday in SHABBOS:
            event = SHABBOS[weekday]
            self.shabbos = event.title
            self.category = event.category

    def _yomtov(self) -> None:
        holidays = YOMTOV if self.diaspora else YOMTOV_ISRAEL
        if (
            self.jewish_date.month in holidays
            and self.jewish_date.day in holidays[self.jewish_date.month]
        ):
            event = holidays[self.jewish_date.month][self.jewish_date.day]
            self.yomtov = event.title

            # don't overwrite category `None` if Chol HaMoed is on Shabbos
            if event.category:
                if not self.category:
                    self.category = event.category
                elif self.category != event.category:
                    # if Shabbos / Yom Tov has Candles / Havdalah, Candles has priority
                    self.category = Category.CANDLES.value

    def _erev(self) -> None:
        is_erev_shabbos = self.shabbos and 'Erev' in self.shabbos

        is_erev_yom_tov = self.yomtov and any(
            [
                'Erev' in self.yomtov,
                'Hoshana Rabba' in self.yomtov,
                'Pesach 6' in self.yomtov,
            ],
        )

        if self.category == 'Candles' and any(
            [
                is_erev_shabbos and not self.yomtov,
                is_erev_shabbos and is_erev_yom_tov,
                is_erev_shabbos and self.yomtov and 'Chol HaMoed' in self.yomtov,
                not is_erev_shabbos and is_erev_yom_tov,
            ],
        ):
            self.is_erev = True

    def _issur_melacha(self) -> None:
        self.is_issur_melacha = self.category is not None and not self.is_erev
