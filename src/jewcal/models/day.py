"""Jewish day model."""

from dataclasses import dataclass, field
from datetime import date as datetime_date
from typing import Iterator, Tuple

from ..helpers.calendars import CalendarGenerator
from .date import Date
from .enums import Fast, Month, Shabbat


@dataclass(slots=True)
class DayCategories:
    """The different day categories."""

    erev: bool = False
    """Is it the day before Shabbat or Yom Tov."""

    shabbat: bool = False
    """Is it Shabbat."""

    yomtov: bool = False
    """Is it Yom Tov."""

    chag: bool = False
    """Is it a Chag."""

    fast: bool = False
    """Is it a Fast day."""

    def __iter__(self) -> Iterator[Tuple[str, bool]]:
        """Iterate through all categories.

        Yields:
            A tuple with the category name and value.
        """
        for category in self.__dataclass_fields__:  # pylint: disable=no-member
            yield category, getattr(self, category)


@dataclass(slots=True)
class Day:
    """A day in the Jewish calendar.

    A day has categories and names for holidays and fasts.
    """

    date: Date
    """The Jewish date."""

    categories: DayCategories
    """The categories."""

    names: list[str]
    """The holiday names."""

    _erev_shabbat: bool = field(repr=False)
    _erev_yomtov: bool = field(repr=False)

    def __init__(self, gregorian: datetime_date, diaspora: bool) -> None:
        """Initialize a day.

        Args:
            gregorian: The Gregorian date.
            diaspora: True if outside of Israel, False if in Israel.
        """
        self.date = Date(gregorian)
        self.categories = DayCategories()
        self.names = []

        self._erev_shabbat = False
        self._erev_yomtov = False

        # shabbat
        weekday = self.date.weekday
        match weekday:
            case 5:
                self.categories.erev = True
                self._erev_shabbat = True
                self.names.append(str(Shabbat.EREV))
            case 6:
                self.categories.shabbat = True
                self.names.append(str(Shabbat.SHABBAT))

        # holiday / fast
        year = self.date.year
        month = Month(self.date.month)
        day = self.date.day
        calendar = CalendarGenerator(diaspora, year).calendar
        events = []
        try:
            calendar[month][day]
        except KeyError:
            pass
        else:
            events.extend(calendar[month][day])

        for event in events:
            attr = event.holiday.__class__.__name__.lower()
            setattr(self.categories, attr, True)

            if event.holiday is Fast.YOM_KIPPUR:
                continue  # don't add Yom Kippur twice to names

            if event.erev:
                self.categories.erev = True
                self._erev_yomtov = True
                self.categories.yomtov = False

            self.names.append(str(event))

    def __str__(self) -> str:
        """Get the day as a readable string.

        Returns:
            The day.
        """
        date = f'{str(self.date)}'

        names = f' {", ".join(self.names)}' if self.names else ''

        return f'{date}{names}'

    def active_categories(self) -> list[str]:
        """Get all the categories where the value is ``True``.

        Returns:
            A list of category names.
        """
        return [category for category, value in self.categories if value]

    def is_holiday(self) -> bool:
        """Is it a holiday.

        Categories taken into account:
            - Shabbat
            - :py:class:`~.enums.YomTov`
            - :py:class:`~.enums.Chag`

        Returns:
            True if holiday, False otherwise.
        """
        if any([
            self.categories.shabbat,
            self.categories.yomtov,
            self.categories.chag,
        ]):
            return True

        return False

    def is_fast_day(self) -> bool:
        """Is it a fast day.

        Fasts taken into account:
            - :py:class:`~.enums.Fast`

        Returns:
            True if a fast day, False otherwise.
        """
        return self.categories.fast

    def is_erev_shabbat(self) -> bool:
        """Is it Erev Shabbat.

        Returns:
            True if Erev Shabbat, False otherwise.
        """
        return self._erev_shabbat

    def is_shabbat(self) -> bool:
        """Is it Shabbat.

        Returns:
            True if Shabbat, False otherwise.
        """
        return self.categories.shabbat

    def is_erev_yomtov(self) -> bool:
        """Is it Erev Yom Tov.

        Returns:
            True if Erev Yom Tov, False otherwise.
        """
        return self._erev_yomtov

    def is_yomtov(self) -> bool:
        """Is it Yom Tov.

        Holidays taken into account:
            - :py:class:`~.enums.YomTov`

        Returns:
            True if Yom Tov, False otherwise.
        """
        return self.categories.yomtov

    def is_issur_melacha(self) -> bool:
        """Is it Issur Melacha (forbidden to work).

        Holidays taken into account:
            - Shabbat
            - :py:class:`~.enums.YomTov`

        Returns:
            True if Issur Melacha, False otherwise.
        """
        return self.categories.shabbat or self.categories.yomtov

    def is_chag(self) -> bool:
        """Is it a Chag.

        Holidays taken into account:
            - :py:class:`~.enums.Chag`

        Returns:
            True if Chag, False otherwise.
        """
        return self.categories.chag
