"""Jewish day model."""

from copy import deepcopy
from dataclasses import dataclass
from datetime import date as datetime_date
from typing import Final, Iterator, Tuple

from ..helpers.calendars import CalendarGenerator, Category, Event
from .date import Date, Months

SHABBAT: Final[dict[int, Event]] = {
    5: Event('Erev Shabbat', [Category.EREV]),
    6: Event('Shabbat', [Category.SHABBAT]),
}


@dataclass(slots=True)
class DayCategories:
    """The different categories of holidays / fast."""

    erev: bool = False
    """Is it the day before Shabbat or Yom Tov."""

    shabbat: bool = False
    """Is it Shabbat."""

    yom_tov: bool = False
    """Is it Yom Tov."""

    chol_hamoed: bool = False
    """Is it Chol HaMoed."""

    chag: bool = False
    """Is it a Chag."""

    rosh_chodesh: bool = False
    """Is it Rosh Chodesh."""

    fast: bool = False
    """Is it a Fast day."""

    def __iter__(self) -> Iterator[Tuple[str, bool]]:
        """Iterate through all categories.

        Yields:
            A tuple with the category name and value.
        """
        for field in self.__dataclass_fields__:  # pylint: disable=no-member
            yield field, getattr(self, field)


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

    def __init__(self, gregorian: datetime_date, diaspora: bool) -> None:
        """Create a day.

        Args:
            gregorian: The Gregorian date.
            diaspora: True if outside of Israel, False if in Israel.
        """
        self.date = Date(gregorian)
        self.categories = DayCategories()
        self.names = []

        events: list[Event] = []
        weekday = self.date.weekday

        # shabbat
        if weekday in (5, 6):
            events.append(SHABBAT[weekday])

        # holiday / fast
        year = self.date.year
        month = Months(self.date.month)
        day = self.date.day
        calendar = CalendarGenerator(diaspora, year).calendar
        try:
            calendar[month][day]
        except KeyError:
            pass
        else:
            events.extend(calendar[month][day])

        # save in self
        for event in events:
            for category in event.categories:
                attr = f'{category.name.lower()}'
                setattr(self.categories, attr, True)

            self.names.append(event.name)

    def __str__(self) -> str:
        """Get the day as a readable string.

        Returns:
            The day.
        """
        date: str = f'{str(self.date)}'

        names: str = f' {", ".join(self.names)}' if self.names else ''

        return f'{date}{names}'

    def active_categories(self) -> list[str]:
        """Get all the categories where the value is ``True``.

        Returns:
            A list of category names.
        """
        return [category for category, value in self.categories if value]

    def is_holiday(self) -> bool:
        """Is it a holiday.

        If any of the categories (except fast) are ``True``.

        Returns:
            True if holiday, False otherwise.
        """
        active_categories = self.active_categories()

        if self.categories.fast:
            try:
                active_categories.remove(Category.FAST.name.lower())
            except ValueError:  # pragma: no cover
                pass

        return len(active_categories) > 0

    def is_fast_day(self) -> bool:
        """Is it a fast day.

        Fast days that fall under this category:
            - Shiva Asar BeTamuz
            - Tisha BeAv
            - Tzom Gedalia
            - Yom Kippur
            - Asara BeTevet
            - TaAnit Esther

        Returns:
            True if a fast day, False otherwise.
        """
        return self.categories.fast

    def is_erev_shabbat(self) -> bool:
        """Is it Erev Shabbat.

        Returns:
            True if Erev Shabbat, False otherwise.
        """
        return self.categories.erev and self.date.weekday == 5

    def is_shabbat(self) -> bool:
        """Is it Shabbat.

        Returns:
            True if Shabbat, False otherwise.
        """
        return self.categories.shabbat

    def is_erev_yom_tov(self) -> bool:
        """Is it Erev Yom Tov.

        Returns:
            True if Erev Yom Tov, False otherwise.
        """
        if self.categories.erev:
            names = deepcopy(self.names)
            try:
                names.remove('Erev Shabbat')
            except ValueError:
                pass

            return 'Erev Shabbat' not in names

        return False

    def is_yom_tov(self) -> bool:
        """Is it Yom Tov.

        Holidays that fall under this category:
            - Pesach (excl. Chol HaMoed)
            - Shavuot
            - Rosh Hashana
            - Yom Kippur
            - Sukkot (excl. Chol HaMoed)
            - Shmini Atzeret
            - Simchat Tora

        Returns:
            True if Yom Tov, False otherwise.
        """
        return self.categories.yom_tov

    def is_issur_melacha(self) -> bool:
        """Is it Issur Melacha (forbidden to work).

        Holidays taken into account:
            - Shabbat
            - Yom Tov

        Returns:
            True if Issur Melacha, False otherwise.
        """
        return self.categories.shabbat or self.categories.yom_tov

    def is_chol_hamoed(self) -> bool:
        """Is it Chol HaMoed.

        Holidays that fall under this category:
            - Pesach: 2nd (3rd in Diaspora) through 6th days.
            - Sukkot: 2nd (3rd in Diaspora) through 7th days.

        Returns:
            True if Chol HaMoed, False otherwise.
        """
        return self.categories.chol_hamoed

    def is_chag(self) -> bool:
        """Is it a Chag.

        Holidays that fall under this category:
            - Isru Chag (the day after each Pesach, Shavuot and Sukkot)
            - Lag BaOmer
            - Chanuka
            - Tu BiShevat
            - Purim
            - Shushan Purim

        Returns:
            True if Chag, False otherwise.
        """
        return self.categories.chag

    def is_rosh_chodesh(self) -> bool:
        """Is it Rosh Chodesh.

        Ooccurs monthly and is 1 or 2 days, depending on the length of the
        month.

        Returns:
            True if Rosh Chodesh, False otherwise.
        """
        return self.categories.rosh_chodesh
