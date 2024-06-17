"""Usage examples for Diaspora and Israel.

Diaspora
--------

>>> from jewcal import JewCal

>>> today = JewCal()  # today's date
>>> pesach_2 = JewCal(date(2022, 4, 17))  # specific date

>>> print(pesach_2.jewish_date)
16 Nisan 5782
>>> print(pesach_2.events)
Pesach 2
>>> print(pesach_2.events.shabbos)
None
>>> print(pesach_2.events.yomtov)
Pesach 2
>>> print(pesach_2.events.action)
Havdalah

>>> print(pesach_2.has_events())
True
>>> print(pesach_2.is_erev())
False
>>> print(pesach_2.is_erev_shabbos())
False
>>> print(pesach_2.is_shabbos())
False
>>> print(pesach_2.is_erev_yomtov())
False
>>> print(pesach_2.is_yomtov())
True
>>> print(pesach_2.is_issur_melacha())
True


Israel
------

>>> today = JewCal(diaspora=False)  # today's date
>>> chol_hamoed_1 = JewCal(date(2022, 4, 17), diaspora=False)  # specific date

>>> print(chol_hamoed_1.jewish_date)
16 Nisan 5782
>>> print(chol_hamoed_1.events)
Chol HaMoed 1 (Pesach 2)
>>> print(chol_hamoed_1.events.shabbos)
None
>>> print(chol_hamoed_1.events.yomtov)
Chol HaMoed 1 (Pesach 2)
>>> print(chol_hamoed_1.events.action)
None

>>> print(chol_hamoed_1.has_events())
True
>>> print(chol_hamoed_1.is_erev())
False
>>> print(chol_hamoed_1.is_erev_shabbos())
False
>>> print(chol_hamoed_1.is_shabbos())
False
>>> print(chol_hamoed_1.is_erev_yomtov())
False
>>> print(chol_hamoed_1.is_yomtov())
False
>>> print(chol_hamoed_1.is_issur_melacha())
False
"""

from datetime import date, datetime, timezone
from warnings import warn

from .constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Action
from .models.events import Events
from .models.jewish_date import JewishDate
from .utils.calculations import (
    absdate_to_jewish,
    gregorian_to_absdate,
    is_jewish_leap,
    weekday_from_absdate,
)


class JewCal:
    """Convert Gregorian to Jewish dates with holidays for Diaspora and Israel."""

    def __init__(
        self,
        gregorian_date: date | None = None,
        *,
        diaspora: bool = True,
    ) -> None:
        """Create a new Jewish date for Diaspora or Israel.

        Args:
            gregorian_date: The Gregorian date to convert from, default is
                `date.today()`.
            diaspora: `True` if outside of Israel, `False` if in Israel.
        """
        self._diaspora: bool = diaspora

        gregorian = (
            gregorian_date if gregorian_date else datetime.now(tz=timezone.utc).date()
        )

        absdate = gregorian_to_absdate(gregorian.year, gregorian.month, gregorian.day)
        year, month, day = absdate_to_jewish(absdate)
        is_leap = is_jewish_leap(year)
        self._jewish_date = JewishDate(year, month, day, gregorian, is_leap)

        self._events = Events()

        self._shabbos(absdate)
        self._yomtov()

    @property
    def diaspora(self) -> bool:
        """Is the schedule for Diaspora or Israel.

        Returns:
            `True` if outside of Israel, `False` if in Israel.
        """
        return self._diaspora

    @property
    def jewish_date(self) -> JewishDate:
        """Get the date in the Jewish calendar.

        Returns:
            The Jewish date.
        """
        return self._jewish_date

    @property
    def events(self) -> Events:
        """Get the events (Shabbos and Yom Tov) with an action (Candles or Havdalah).

        Returns:
            The events.
        """
        return self._events

    def __str__(self) -> str:
        """The Jewish date and events as a string.

        Returns:
            The Jewish date and events.
        """
        date_str = self._jewish_date.__str__()
        events_str = self._events.__str__()

        if events_str:
            return f'{date_str}: {events_str}'

        return date_str

    def __repr__(self) -> str:
        """Get a printable representation.

        Returns:
            The `JewCal` object as a printable representation.
        """
        return (
            f'{self.__class__.__name__}('
            f'jewish_date={self._jewish_date.__repr__()},'
            f' events={self._events.__repr__()},'
            f' diaspora={self._diaspora}'
            ')'
        )

    @property
    def year(self) -> int:
        """Get the year in the Jewish calendar.

        .. deprecated:: 0.6.0 Use :py:attr:`jewish_date` ``.year``

        Returns:
            The year in the Jewish calendar.
        """
        warn('year is deprecated, use jewish_date.year', stacklevel=2)
        year: int = self._jewish_date.year
        return year

    @property
    def month(self) -> int:
        """Get the month in the Jewish year.

        .. deprecated:: 0.6.0 Use :py:attr:`jewish_date` ``.month``

        Returns:
            The month in the Jewish year.
        """
        warn('month is deprecated, use jewish_date.month', stacklevel=2)
        month: int = self._jewish_date.month
        return month

    @property
    def day(self) -> int:
        """Get the day in the Jewish month.

        .. deprecated:: 0.6.0 Use :py:attr:`jewish_date` ``.day``

        Returns:
            The day in the Jewish month.
        """
        warn('day is deprecated, use jewish_date.day', stacklevel=2)
        day: int = self._jewish_date.day
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
        gregorian_date: date = self._jewish_date.gregorian_date
        return gregorian_date

    @property
    def shabbos(self) -> str | None:
        """Get the (Erev) Shabbos definition.

        .. deprecated:: 0.6.0 Use :py:attr:`events` ``.shabbos``

        Returns:
            The (Erev) Shabbos definition.
        """
        warn('shabbos is deprecated, use events.shabbos', stacklevel=2)
        return self._events.shabbos

    @property
    def yomtov(self) -> str | None:
        """Get the (Erev) Yom Tov definition.

        .. deprecated:: 0.6.0 Use :py:attr:`events` ``.yomtov``

        Returns:
            The (Erev) Yom Tov definition.
        """
        warn('yomtov is deprecated, use events.yomtov', stacklevel=2)
        return self._events.yomtov

    @property
    def category(self) -> str | None:
        """Get the category (`Candles` or `Havdalah`).

        .. deprecated:: 0.6.0 Use :py:attr:`events` ``.action``

        Returns:
            The category (`Candles` or `Havdalah`).
        """
        warn('category is deprecated, use events.action', stacklevel=2)
        return self._events.action

    def _shabbos(self, absdate: int) -> None:
        weekday: int = weekday_from_absdate(absdate)
        if weekday in SHABBOS:
            event = SHABBOS[weekday]
            self._events.shabbos = event.title
            self._events.action = event.action

    def _yomtov(self) -> None:
        month = self._jewish_date.month
        day = self._jewish_date.day

        holidays = YOMTOV if self._diaspora else YOMTOV_ISRAEL
        if month in holidays and day in holidays[month]:
            event = holidays[month][day]
            self._events.yomtov = event.title

            # don't overwrite action `None` if Chol HaMoed is on Shabbos
            if event.action:
                if not self._events.action:
                    self._events.action = event.action
                elif self._events.action != event.action:
                    # if Shabbos / Yom Tov has Candles / Havdalah, Candles has priority
                    self._events.action = Action.CANDLES.value

    def has_events(self) -> bool:
        """Are there any events [(Erev) Shabbos or (Erev) Yom Tov].

        Returns:
            `True` if there are any events, `False` otherwise.
        """
        # pylint: disable=W0212
        return self._events._has_events()  # noqa: SLF001 Private member accessed

    def is_erev_shabbos(self) -> bool:
        """Is it Erev Shabbos.

        Returns:
            `True` if it is Erev Shabbos, `False` otherwise.
        """
        # pylint: disable=W0212
        return self._events._is_erev_shabbos()  # noqa: SLF001 Private member accessed

    def is_shabbos(self) -> bool:
        """Is it Shabbos.

        Returns:
            `True` if it is Shabbos, `False` otherwise.
        """
        # pylint: disable=W0212
        return self._events._is_shabbos()  # noqa: SLF001 Private member accessed

    def is_erev_yomtov(self) -> bool:
        """Is it Erev Yom Tov.

        Returns:
            `True` if it is Erev Yom Tov, `False` otherwise.
        """
        # pylint: disable=W0212
        return self._events._is_erev_yomtov()  # noqa: SLF001 Private member accessed

    def is_yomtov(self) -> bool:
        """Is it Yom Tov.

        Chol HaMoed is not considered Yom Tov.

        Returns:
            `True` if it is Yom Tov, `False` otherwise.
        """
        # pylint: disable=W0212
        return self._events._is_yomtov()  # noqa: SLF001 Private member accessed

    def is_erev(self) -> bool:
        """Is it Erev Shabbos and/or Erev Yom Tov.

        Returns:
            `True` if it is Erev Shabbos and/or Erev Yom Tov, `False` otherwise.
        """
        # pylint: disable=W0212
        return self._events._is_erev()  # noqa: SLF001 Private member accessed

    def is_issur_melacha(self) -> bool:
        """Is it Issur Melacha.

        Returns:
            `True` if it is Issur Melacha, `False` otherwise.
        """
        # pylint: disable=W0212
        return self._events._is_issur_melacha()  # noqa: SLF001 Private member accessed
