"""Jewish Calendar Generator."""

from __future__ import annotations

from dataclasses import dataclass
from logging import getLogger
from typing import Optional

from ..models.enums import CalendarType, Chag, Fast, Month, YomTov
from .dates import (_days_in_jewish_month, _is_jewish_leap, _is_short_kislev,
                    _weekday_from_jewish)

logger = getLogger(__name__)


@dataclass(slots=True)
class Event():
    """The calendar event."""

    holiday: YomTov | Chag | Fast
    description: Optional[str] = None
    erev: bool = False
    day: int = 0

    def __str__(self) -> str:
        """Get the event as a readable string.

        Returns:
            The event.
        """
        erev = 'Erev ' \
            if self.erev and isinstance(self.holiday, YomTov) else ''

        holiday = str(self.holiday) \
            if not self.description else self.description

        day = f' {self.day}' if self.day else ''

        return f'{erev}{holiday}{day}'


TYearDict = dict[Month, dict[int, list[Event]]]


class Singleton(type):
    """Singleton to restrict the instantiation to one 'single' instance."""

    # https://stackoverflow.com/a/6798042 create
    # https://stackoverflow.com/a/50065732 clear

    _instances: dict[Singleton, Singleton] = {}

    def __call__(cls, *args, **kwargs):  # type: ignore[no-untyped-def]
        """Return the instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The instance.
        """
        if cls not in cls._instances:
            logger.info('Returning new Singleton instance')

            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        else:
            logger.info('Returning existing Singleton instance')

        return cls._instances[cls]

    def clear(cls) -> None:  # pragma: no cover
        """Reset Singleton for unittests."""
        try:
            del Singleton._instances[cls]
            logger.info('Singleton instance reset')
        except KeyError:
            pass


class CalendarsCache(metaclass=Singleton):
    """Cache generated calendars.

    Uses the Singleton pattern.
    """

    calendars: dict[CalendarType, dict[int, TYearDict]]
    """The cached calendars."""

    def __init__(self) -> None:
        """Initialize the cache."""
        self.calendars = {
            CalendarType.DIASPORA: {},
            CalendarType.ISRAEL: {},
        }

    def add(
        self,
        year: int,
        calendar: TYearDict,
        calendar_type: CalendarType
    ) -> None:
        """Add a new calendar to the cache.

        Args:
            year: The Jewish calendar year.
            calendar: The calendar to store.
            calendar_type: Is the calendar for Diaspora or Israel.
        """
        logger.info(
            'Calendar for %s added to Singleton',
            (year, calendar_type.name)
        )

        self.calendars[calendar_type][year] = calendar

    def get(
        self,
        year: int,
        calendar_type: CalendarType
    ) -> Optional[TYearDict]:
        """Get a cached calendar.

        Args:
            year: The Jewish calendar year.
            calendar_type: Is the calendar for Diaspora or Israel.

        Returns:
            The calendar.
        """
        logger.info(
            'Calendar for %s requested from Singleton',
            (year, calendar_type.name)
        )

        if year in self.calendars[calendar_type]:
            return self.calendars[calendar_type][year]

        return None


@dataclass(slots=True, repr=False)
class CalendarGenerator:
    """Jewish calendar generator.

    - Israel and Diaspora use a different calendar.
    - Chanuka is adjusted depending on the amount of days in Kislev.
    - A Jewish year has an extra month (Adar 2) if it is a leap year.
    - If fast days occur on Shabbat, some fast days are moved up or postponed.
    - Rosh Chodesh is one or two days, depending on the month.
    """

    calendar: TYearDict
    """The Jewish calendar."""

    year: int
    """The Jewish year."""

    leap: bool
    """Is it a Jewish leap year."""

    calendar_type: CalendarType
    """Is the calendar for Israel or Diaspora."""

    def __init__(self, diaspora: bool, jewish_year: int) -> None:
        """Initialize the calendar.

        Args:
            diaspora: True if outside of Israel, False if in Israel.
            jewish_year: The Jewish year.

        Raises:
            TypeError: If diaspora or jewish_year have an unsupported type.
        """
        if not isinstance(diaspora, bool):
            raise TypeError(f'unsupported type {diaspora.__class__.__name__}')

        if not isinstance(jewish_year, int):
            raise TypeError(
                f'unsupported type {jewish_year.__class__.__name__}'
            )

        self.year = jewish_year
        self.leap = _is_jewish_leap(self.year)
        self.calendar = {}
        self.calendar_type = \
            CalendarType.DIASPORA if diaspora else CalendarType.ISRAEL

        # singleton to cache calendars
        cache = CalendarsCache()
        calendar = cache.get(self.year, self.calendar_type)

        if calendar:
            # calendar already in cache
            self.calendar = calendar
        else:
            # add to cache
            cache.add(self.year, self.calendar, self.calendar_type)

            # months
            if self.leap:
                for i in range(0, 13):
                    self.calendar[Month.get(i + 1, self.leap)] = {}
            else:
                for i in range(0, 12):
                    self.calendar[Month(i + 1)] = {}

            # holidays / fasts
            self._pesach()
            self._lag_baomer()
            self._shavuot()
            self._rosh_hashana_yom_kippur()
            self._sukkot()
            self._chanuka()
            self._tu_bishvat()
            self._purim_and_shushan()
            self._rosh_chodesh()
            self._fast_days()

    def _pesach(self) -> None:
        """Set Pesach."""
        # 1st day(s)
        events = self._yomtov(YomTov.PESACH)

        # Chol HaMoed
        events.extend(self._chol_hamoed(Chag.PESACH_CHOL_HAMOED))
        events[-1][0].erev = True

        # last day(s)
        events.append([Event(YomTov.PESACH, day=7)])

        if self.calendar_type is CalendarType.DIASPORA:
            events.append([Event(YomTov.PESACH, day=8)])

        # Isru Chag
        events.append([Event(Chag.ISRU_CHAG)])

        # save
        day_of_month = 14
        for i, event in enumerate(events):
            self.calendar[Month.NISAN][day_of_month + i] = event

    def _lag_baomer(self) -> None:
        """Set Lag BaOmer."""
        self.calendar[Month.IYAR][18] = [Event(Chag.LAG_BAOMER)]

    def _shavuot(self) -> None:
        """Set Shavuot."""
        # 1st day(s)
        events = self._yomtov(YomTov.SHAVUOT)

        # Isru Chag
        events.append([Event(Chag.ISRU_CHAG)])

        # save
        day_of_month = 5
        for i, event in enumerate(events):
            self.calendar[Month.SIVAN][day_of_month + i] = event

    def _rosh_hashana_yom_kippur(self) -> None:
        """Set Rosh Hashana and Yom Kippur."""
        # Rosh Hashana
        self.calendar[Month.ELUL][29] = [Event(YomTov.ROSH_HASHANA, erev=True)]
        self.calendar[Month.TISHREI][1] = [Event(YomTov.ROSH_HASHANA, day=1)]
        self.calendar[Month.TISHREI][2] = [Event(YomTov.ROSH_HASHANA, day=2)]

        # Yom Kippur
        self.calendar[Month.TISHREI][9] = [Event(YomTov.YOM_KIPPUR, erev=True)]
        self.calendar[Month.TISHREI][10] = [
            Event(YomTov.YOM_KIPPUR), Event(Fast.YOM_KIPPUR),
        ]

    def _sukkot(self) -> None:
        """Set Sukkot."""
        # 1st day(s)
        events = self._yomtov(YomTov.SUKKOT)

        # Chol HaMoed
        events.extend(self._chol_hamoed(Chag.SUKKOT_CHOL_HAMOED))

        # Hoshana Raba
        events.append([Event(Chag.HOSHANA_RABA, erev=True)])

        # Shmini Atzeret, Simchat Tora
        if self.calendar_type is CalendarType.ISRAEL:
            events.append([
                Event(YomTov.SHMINI_ATZERET), Event(YomTov.SIMCHAT_TORA)
            ])
        else:
            events.append([Event(YomTov.SHMINI_ATZERET)])
            events.append([Event(YomTov.SIMCHAT_TORA)])

        # Isru Chag
        events.append([Event(Chag.ISRU_CHAG)])

        # save
        day_of_month = 14
        for i, event in enumerate(events):
            self.calendar[Month.TISHREI][day_of_month + i] = event

    def _chanuka(self) -> None:
        """Set Chanuka.

        Chanuka is adjusted depending on the amount of days in Kislev.
        """
        is_short_kislev = _is_short_kislev(self.year)
        day = 0  # count to 8 days

        # Kislev
        day_of_month = 25

        for i in range(0, 5):
            day += 1

            self.calendar[Month.KISLEV][day_of_month + i] = [
                Event(Chag.CHANUKA, day=day)
            ]

        if not is_short_kislev:
            day += 1

            self.calendar[Month.KISLEV][30] = [Event(Chag.CHANUKA, day=day)]

        # Tevet
        day_of_month = 1

        stop = 3 if is_short_kislev else 2

        for i in range(0, stop):
            day += 1

            self.calendar[Month.TEVET][day_of_month + i] = [
                Event(Chag.CHANUKA, day=day)
            ]

    def _tu_bishvat(self) -> None:
        """Set Tu BiShvat."""
        self.calendar[Month.SHEVAT][15] = [Event(Chag.TU_BISHVAT)]

    def _purim_and_shushan(self) -> None:
        """Set Purim and Shushan Purim.

        If the Jewish year is a leap year, Purim and Shushan Purim are
        celebrated in Adar 2.
        """
        month = Month.ADAR_2 if self.leap else Month.ADAR

        self.calendar[month][14] = [Event(Chag.PURIM)]
        self.calendar[month][15] = [Event(Chag.SHUSHAN_PURIM)]

    def _rosh_chodesh(self) -> None:
        """Set Rosh Chodesh for each month.

        Rosh Chodesh is 1 or 2 days, depending on the length of the month.
        """
        for month in list(self.calendar.keys()):
            # skip Tishrei - Rosh Hashana
            if month.value + 1 == 7:
                continue

            # next month
            match month.value:
                case 12 | 13:  # Adar or Adar 2
                    next_month_index = 1  # Nisan
                case 14:  # Adar 1
                    next_month_index = 13  # Adar 2
                case _:
                    next_month_index = month.value + 1

            next_month = Month.get(next_month_index, self.leap)

            # event
            event = Event(
                Chag.ROSH_CHODESH,
                description=f'{Chag.ROSH_CHODESH} {next_month}'
            )

            # save
            if _days_in_jewish_month(self.year, month.value) == 30:
                self.calendar[month].setdefault(30, []).append(event)

            self.calendar[next_month].setdefault(1, []).append(event)

    def _fast_days(self) -> None:
        """Set fast days.

        - Some fast are postponed until Sunday if they fall on Shabbat.
        - If TaAnit Esther falls on Shabbat, it is moved up to Thursday.
        - If the Jewish year is a leap year, TaAnit Esther falls in Adar 2.
        """
        # Shiva Asar BeTamuz
        event = [Event(Fast.TAMUZ_17)]

        if _weekday_from_jewish(self.year, Month.TAMUZ, 17) == 6:
            self.calendar[Month.TAMUZ][18] = event
        else:
            self.calendar[Month.TAMUZ][17] = event

        # Tisha BeAv
        event = [Event(Fast.AV_9)]

        if _weekday_from_jewish(self.year, Month.AV, 9) == 6:
            self.calendar[Month.AV][10] = event
        else:
            self.calendar[Month.AV][9] = event

        # Tzom Gedalia
        event = [Event(Fast.TZOM_GEDALIA)]

        if _weekday_from_jewish(self.year, Month.TISHREI, 3) == 6:
            self.calendar[Month.TISHREI][4] = event
        else:
            self.calendar[Month.TISHREI][3] = event

        # Asara BeTevet
        self.calendar[Month.TEVET][10] = [Event(Fast.TEVET_10)]

        # TaAnit Esther
        event = [Event(Fast.TANIT_ESTHER)]
        month = Month.ADAR_2 if self.leap else Month.ADAR

        if _weekday_from_jewish(self.year, month, 13) == 6:
            self.calendar[month][11] = event
        else:
            self.calendar[month][13] = event

    def _yomtov(self, yom_tov: YomTov) -> list[list[Event]]:
        """Set Yom Tov.

        Args:
            yom_tov: The Yom Tov.

        Returns:
            A list of events.
        """
        events = [[Event(yom_tov, erev=True)]]

        if self.calendar_type is CalendarType.ISRAEL:
            events.append([Event(yom_tov)])
        else:
            for i in range(2):
                events.append([Event(yom_tov, day=i + 1)])

        return events

    def _chol_hamoed(self, chol_hamoed: Chag) -> list[list[Event]]:
        """Set Chol HaMoed.

        Args:
            chol_hamoed: The Chol HaMoed.

        Returns:
            A list of events.
        """
        length = 5 if self.calendar_type is CalendarType.ISRAEL else 4

        events = []
        for i in range(0, length):
            events.append([Event(chol_hamoed, day=i + 1)])

        return events
