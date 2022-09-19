"""Jewish Calendar Generator."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, unique
from logging import getLogger
from typing import Optional

from ..models.date import Months
from .dates import (_days_in_jewish_month, _is_jewish_leap, _is_short_kislev,
                    _weekday_from_jewish)

logger = getLogger(__name__)


@unique
class Category(Enum):
    """The `Event` categories."""

    EREV = 'Erev'
    SHABBAT = 'Shabbat'
    YOM_TOV = 'Yom Tov'
    CHOL_HAMOED = 'Chol HaMoed'
    CHAG = 'Chag'
    ROSH_CHODESH = 'Rosh Chodesh'
    FAST = 'Tzom'


@dataclass(slots=True)
class Event():
    """The calendar event."""

    name: str
    categories: list[Category]


TYearDict = dict[Months, dict[int, list[Event]]]


@unique
class CalendarType(Enum):
    """The calendar types."""

    DIASPORA = 'Diaspora'
    ISRAEL = 'Israel'


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

    - Diaspora and Israel use a different calendar.
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

    def __init__(self, diaspora: bool, jewish_year: int) -> None:
        """Create the calendar.

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

        # singleton to cache calendars
        calendar_type = \
            CalendarType.DIASPORA if diaspora else CalendarType.ISRAEL
        cache = CalendarsCache()
        calendar = cache.get(self.year, calendar_type)

        if calendar:
            # calendar already in cache
            self.calendar = calendar
        else:
            # generate new calendar and add to cache
            self.calendar = deepcopy(DIASPORA if diaspora else ISRAEL)
            cache.add(self.year, self.calendar, calendar_type)

            # set / adjust holidays
            self._postpone_fastdays()
            self._set_chanuka_and_asara_betevet()
            self._set_tanit_esther_and_purim()
            self._set_rosh_chodesh()

    def _postpone_fastdays(self) -> None:
        """Postpone fasts if they occur on Shabbat.

        If a fast day falls on Shabbat, it is postponed until Sunday.
        """
        # Shiva Asar BeTamuz
        if _weekday_from_jewish(self.year, Months.TAMUZ, 17) == 6:
            self.calendar[Months.TAMUZ][18] = \
                self.calendar[Months.TAMUZ][17]
            self.calendar[Months.TAMUZ].pop(17)

        # Tisha BeAv
        if _weekday_from_jewish(self.year, Months.AV, 9) == 6:
            self.calendar[Months.AV][10] = self.calendar[Months.AV][9]
            self.calendar[Months.AV].pop(9)

        # Tzom Gedaliah
        if _weekday_from_jewish(self.year, Months.TISHREI, 3) == 6:
            self.calendar[Months.TISHREI][4] = \
                self.calendar[Months.TISHREI][3]
            self.calendar[Months.TISHREI].pop(3)

    def _set_chanuka_and_asara_betevet(self) -> None:
        """Set Chanuka and Asara BeTevet.

        Chanuka is adjusted depending on the amount of days in Kislev.
        """
        # Chanuka
        if _is_short_kislev(self.year):
            self.calendar[Months.TEVET] = CHANUKA_SHORT_KISLEV[Months.TEVET]
        else:
            self.calendar[Months.KISLEV][30] = \
                CHANUKA_LONG_KISLEV[Months.KISLEV][30]
            self.calendar[Months.TEVET] = CHANUKA_LONG_KISLEV[Months.TEVET]

        # Asara BeTevet
        self.calendar[Months.TEVET][10] = \
            [Event('Asara BeTevet', [Category.FAST])]

    def _set_tanit_esther_and_purim(self) -> None:
        """Set TaAnit Esther and Purim.

        - If TaAnit Esther falls on Shabbat, it is moved up to Thursday.
        - If the Jewish year is a leap year, Purim is celebrated in Adar 2.
        """
        # Purim
        if self.leap:
            # Adar 2
            self.calendar[Months.ADAR_2] = self.calendar[Months.ADAR]
            self.calendar.pop(Months.ADAR)

            # TaAnit Esther
            if _weekday_from_jewish(self.year, Months.ADAR_2, 13) == 6:
                self.calendar[Months.ADAR_2][11] = \
                    self.calendar[Months.ADAR_2][13]
                self.calendar[Months.ADAR_2].pop(13)
        else:
            # TaAnit Esther
            if _weekday_from_jewish(self.year, Months.ADAR, 13) == 6:
                self.calendar[Months.ADAR][11] = \
                    self.calendar[Months.ADAR][13]
                self.calendar[Months.ADAR].pop(13)

    def _set_rosh_chodesh(self) -> None:
        """Set Rosh Chodesh for each month.

        Rosh Chodesh is 1 or 2 days, depending on the length of the month.
        """
        for month in Months:
            # skip Tishrei - Rosh Hashana
            if month.value + 1 == 7:
                continue

            # set next month
            month_index = month.value
            next_month_index = month_index

            match month_index:
                case Months.ADAR:
                    if self.leap:
                        next_month_index = 13
                    else:
                        next_month_index = 1
                case Months.ADAR_2:
                    next_month_index = 1
                case _:
                    next_month_index += 1

            # create event
            if self.leap and next_month_index == 12:
                next_month_name = 'Adar 1'
            else:
                next_month_name = str(Months(next_month_index))
            event = Event(
                f'Rosh Chodesh {next_month_name}', [Category.ROSH_CHODESH]
            )

            # save event
            # 30th of the month
            if _days_in_jewish_month(self.year, month_index) == 30:
                day = self.calendar \
                    .setdefault(Months(month_index), {}) \
                    .setdefault(30, [])
                if event not in day:
                    day.append(event)

            # 1st of the month
            day = self.calendar \
                .setdefault(Months(next_month_index), {}) \
                .setdefault(1, [])
            if event not in day:
                day.append(event)


ISRAEL: TYearDict = {
    Months.NISAN: {
        14: [Event('Erev Pesach', [Category.EREV])],
        15: [Event('Pesach 1', [Category.YOM_TOV])],
        16: [Event('Chol HaMoed 1 (Pesach 2)', [Category.CHOL_HAMOED])],
        17: [Event('Chol HaMoed 2 (Pesach 3)', [Category.CHOL_HAMOED])],
        18: [Event('Chol HaMoed 3 (Pesach 4)', [Category.CHOL_HAMOED])],
        19: [Event('Chol HaMoed 4 (Pesach 5)', [Category.CHOL_HAMOED])],
        20: [
                Event(
                    'Chol HaMoed 5 (Pesach 6)',
                    [Category.CHOL_HAMOED, Category.EREV]
                )
            ],
        21: [Event('Pesach 7', [Category.YOM_TOV])],
        22: [Event('Isru Chag', [Category.CHAG])],
    },
    Months.IYAR: {
        18: [Event('Lag BaOmer', [Category.CHAG])],
    },
    Months.SIVAN: {
        5: [Event('Erev Shavuot', [Category.EREV])],
        6: [Event('Shavuot 1', [Category.YOM_TOV])],
        7: [Event('Isru Chag', [Category.CHAG])],
    },
    Months.TAMUZ: {
        17: [Event('Shiva Asar BeTamuz', [Category.FAST])],
    },
    Months.AV: {
        9: [Event('Tisha BeAv', [Category.FAST])],
    },
    Months.ELUL: {
        29: [Event('Erev Rosh Hashana', [Category.EREV])],
    },
    Months.TISHREI: {
        1: [Event('Rosh Hashana 1', [Category.YOM_TOV])],
        2: [Event('Rosh Hashana 2', [Category.YOM_TOV])],
        3: [Event('Tzom Gedalia', [Category.FAST])],

        9: [Event('Erev Yom Kippur', [Category.EREV])],
        10: [Event('Yom Kippur', [Category.YOM_TOV, Category.FAST])],

        14: [Event('Erev Sukkot', [Category.EREV])],
        15: [Event('Sukkot 1', [Category.YOM_TOV])],
        16: [Event('Chol HaMoed 1 (Sukkot 2)', [Category.CHOL_HAMOED])],
        17: [Event('Chol HaMoed 2 (Sukkot 3)', [Category.CHOL_HAMOED])],
        18: [Event('Chol HaMoed 3 (Sukkot 4)', [Category.CHOL_HAMOED])],
        19: [Event('Chol HaMoed 4 (Sukkot 5)', [Category.CHOL_HAMOED])],
        20: [Event('Chol HaMoed 5 (Sukkot 6)', [Category.CHOL_HAMOED])],
        21: [
                Event(
                    'Hoshana Rabba (Sukkot 7)',
                    [Category.CHOL_HAMOED, Category.EREV]
                )
            ],
        22: [Event('Shmini Atzeret, Simchat Tora', [Category.YOM_TOV])],
        23: [Event('Isru Chag', [Category.CHAG])],
    },
    Months.KISLEV: {
        25: [Event('Chanuka 1', [Category.CHAG])],
        26: [Event('Chanuka 2', [Category.CHAG])],
        27: [Event('Chanuka 3', [Category.CHAG])],
        28: [Event('Chanuka 4', [Category.CHAG])],
        29: [Event('Chanuka 5', [Category.CHAG])],
    },
    Months.SHEVAT: {
        15: [Event('Tu BiShevat', [Category.CHAG])],
    },
    Months.ADAR: {
        13: [Event('TaAnit Esther', [Category.FAST])],
        14: [Event('Purim', [Category.CHAG])],
        15: [Event('Shushan Purim', [Category.CHAG])],
    },
}

# Diaspora: copy ISRAEL
DIASPORA: TYearDict = deepcopy(ISRAEL)

# Adjust Pesach
DIASPORA[Months.NISAN][16] = \
    [Event('Pesach 2', [Category.YOM_TOV])]
DIASPORA[Months.NISAN][17] = \
    [Event('Chol HaMoed 1 (Pesach 3)', [Category.CHOL_HAMOED])]
DIASPORA[Months.NISAN][18] = \
    [Event('Chol HaMoed 2 (Pesach 4)', [Category.CHOL_HAMOED])]
DIASPORA[Months.NISAN][19] = \
    [Event('Chol HaMoed 3 (Pesach 5)', [Category.CHOL_HAMOED])]
DIASPORA[Months.NISAN][20] = \
    [Event('Chol HaMoed 4 (Pesach 6)', [Category.CHOL_HAMOED, Category.EREV])]
DIASPORA[Months.NISAN][22] = \
    [Event('Pesach 8', [Category.YOM_TOV])]
DIASPORA[Months.NISAN][23] = ISRAEL[Months.NISAN][22]  # Isru Chag

# Adjust Shavuot
DIASPORA[Months.SIVAN][7] = [Event('Shavuot 2', [Category.YOM_TOV])]
DIASPORA[Months.SIVAN][8] = ISRAEL[Months.SIVAN][7]  # Isru Chag

# Adjust Sukkot
DIASPORA[Months.TISHREI][16] = [Event('Sukkot 2', [Category.YOM_TOV])]
DIASPORA[Months.TISHREI][17] = \
    [Event('Chol HaMoed 1 (Sukkot 3)', [Category.CHOL_HAMOED])]
DIASPORA[Months.TISHREI][18] = \
    [Event('Chol HaMoed 2 (Sukkot 4)', [Category.CHOL_HAMOED])]
DIASPORA[Months.TISHREI][19] = \
    [Event('Chol HaMoed 3 (Sukkot 5)', [Category.CHOL_HAMOED])]
DIASPORA[Months.TISHREI][20] = \
    [Event('Chol HaMoed 4 (Sukkot 6)', [Category.CHOL_HAMOED])]
DIASPORA[Months.TISHREI][22] = [Event('Shmini Atzeret', [Category.YOM_TOV])]
DIASPORA[Months.TISHREI][23] = [Event('Simchat Tora', [Category.YOM_TOV])]
DIASPORA[Months.TISHREI][24] = ISRAEL[Months.TISHREI][23]  # Isru Chag

# Chanuka - Kislev has 29 days
CHANUKA_SHORT_KISLEV: TYearDict = {
    Months.TEVET: {
        1: [Event('Chanuka 6', [Category.CHAG])],
        2: [Event('Chanuka 7', [Category.CHAG])],
        3: [Event('Chanuka 8', [Category.CHAG])],
    },
}

# Chanuka - Kislev has 30 days
CHANUKA_LONG_KISLEV: TYearDict = {
    Months.KISLEV: {
        30: [Event('Chanuka 6', [Category.CHAG])],
    },
    Months.TEVET: {
        1: [Event('Chanuka 7', [Category.CHAG])],
        2: [Event('Chanuka 8', [Category.CHAG])],
    },
}
