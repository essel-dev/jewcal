"""Unittests for jewcal.models.day."""

from datetime import date
from unittest import TestCase

from src.jewcal.models.date import Date
from src.jewcal.models.day import Day


class DayTestCase(TestCase):
    """Unittests for `Day`."""

    def test__init___has_no_event(self) -> None:
        """Test __init__  no event and no category."""
        gregorian = date(2022, 9, 1)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertFalse(day.names)

    def test__init__event_category_erev(self) -> None:
        """Test __init__  event with category Erev."""
        gregorian = date(2022, 9, 25)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, True)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Erev Rosh Hashana'])

    def test__init__event_category_shabbat(self) -> None:
        """Test __init__  event with category Shabbat."""
        gregorian = date(2022, 9, 3)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Shabbat'])

    def test__init__event_category_yom_tov(self) -> None:
        """Test __init__  event with category Yom Tov."""
        gregorian = date(2022, 9, 27)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, True)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Rosh Hashana 2'])

    def test__init__event_category_chol_hamoed(self) -> None:
        """Test __init__  event with category Chol HaMoed."""
        # diaspora
        gregorian = date(2022, 4, 18)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Chol HaMoed 1 (Pesach 3)'])

        # Israel
        gregorian = date(2022, 4, 18)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Chol HaMoed 2 (Pesach 3)'])

    def test__init__event_category_chag(self) -> None:
        """Test __init__  event with category Chag."""
        gregorian = date(2022, 12, 19)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Chanuka 1'])

    def test__init__event_category_fast(self) -> None:
        """Test __init__  event with category Fast."""
        gregorian = date(2021, 6, 27)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, True)

        self.assertEqual(day.names, ['Shiva Asar BeTamuz'])

    def test__init__event_shabbat_chol_hamoed_havdala(self) -> None:
        """Test __init__ event Shabbat and Chol Hamoed."""
        # diaspora
        gregorian = date(2021, 9, 25)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(
            day.names,
            ['Shabbat', 'Chol HaMoed 3 (Sukkot 5)']
        )

        # Israel
        gregorian = date(2021, 9, 25)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(
            day.names,
            ['Shabbat', 'Chol HaMoed 4 (Sukkot 5)']
        )

    def test__init__event_shabbat_yom_tov_second_day_havdala(self) -> None:
        """Test __init__ event Shabbat and Shavuot 2."""
        # diaspora
        gregorian = date(2023, 5, 27)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.yom_tov, True)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Shabbat', 'Shavuot 2'])

        # Israel
        gregorian = date(2023, 5, 27)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Shabbat', 'Isru Chag'])

    def test__init__event_erev_shabbat_erev_yom_tov(self) -> None:
        """Test __init__ event Erev Shabbat and Erev Yom Tov."""
        gregorian = date(2022, 4, 15)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, True)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, False)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Erev Shabbat', 'Erev Pesach'])

    def test__init__event_shabbat__yom_tov(self) -> None:
        """Test __init__ event Shabbat and Yom Tov."""
        gregorian = date(2022, 4, 16)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.yom_tov, True)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Shabbat', 'Pesach 1'])

    def test__init__event_yom_tov_fast(self) -> None:
        """Test __init__ event Yom Tov and Fast."""
        gregorian = date(2022, 10, 5)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.yom_tov, True)
        self.assertEqual(day.categories.chol_hamoed, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.rosh_chodesh, False)
        self.assertEqual(day.categories.fast, True)

        self.assertEqual(day.names, ['Yom Kippur'])

    def test__str__(self) -> None:
        """Test __str__."""
        gregorian = date(2022, 9, 1)
        day = Day(gregorian, diaspora=True)
        self.assertEqual(str(day), '5 Elul 5782 (2022-09-01)')

        # diaspora, Israel
        gregorian = date(2022, 4, 16)
        day = Day(gregorian, diaspora=True)
        self.assertEqual(
            str(day),
            '15 Nisan 5782 (2022-04-16) Shabbat, Pesach 1'
        )

        # diaspora
        gregorian = date(2022, 4, 18)
        day = Day(gregorian, diaspora=True)
        self.assertEqual(
            str(day),
            '17 Nisan 5782 (2022-04-18) Chol HaMoed 1 (Pesach 3)'
        )

        # Israel
        gregorian = date(2022, 4, 18)
        day = Day(gregorian, diaspora=False)
        self.assertEqual(
            str(day),
            '17 Nisan 5782 (2022-04-18) Chol HaMoed 2 (Pesach 3)'
        )
