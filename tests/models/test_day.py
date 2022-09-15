"""Unittests for jewcal.models.day."""

from datetime import date
from unittest import TestCase

from src.jewcal.models.date import Date
from src.jewcal.models.day import Day


class DayTestCase(TestCase):
    """Unittests for `Day`."""

    def test__slots__fail(self) -> None:
        """Test __slots__ should fail."""
        jewish_day = Day(date(2022, 9, 1), diaspora=True)

        with self.assertRaises(AttributeError):
            # pylint: disable-next=protected-access, unused-private-member
            jewish_day.__jewish_date = 'x'  # type: ignore[assignment]

        with self.assertRaises(AttributeError):
            # pylint: disable-next=assigning-non-slot
            jewish_day.x = 'x'  # type: ignore[attr-defined]

    def test__init___has_no_event(self) -> None:
        """Test __init__  no event and no category."""
        gregorian = date(2022, 9, 1)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertFalse(jewish_day.names)

    def test__init__event_category_erev(self) -> None:
        """Test __init__  event with category Erev."""
        gregorian = date(2022, 9, 25)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, True)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Erev Rosh Hashana'])

    def test__init__event_category_shabbat(self) -> None:
        """Test __init__  event with category Shabbat."""
        gregorian = date(2022, 9, 3)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, True)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Shabbat'])

    def test__init__event_category_yom_tov(self) -> None:
        """Test __init__  event with category Yom Tov."""
        gregorian = date(2022, 9, 27)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, True)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Rosh Hashana 2'])

    def test__init__event_category_chol_hamoed(self) -> None:
        """Test __init__  event with category Chol HaMoed."""
        # diaspora
        gregorian = date(2022, 4, 18)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, True)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Chol HaMoed 1 (Pesach 3)'])

        # Israel
        gregorian = date(2022, 4, 18)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, True)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Chol HaMoed 2 (Pesach 3)'])

    def test__init__event_category_chag(self) -> None:
        """Test __init__  event with category Chag."""
        gregorian = date(2022, 12, 19)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, True)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Chanuka 1'])

    def test__init__event_category_fast(self) -> None:
        """Test __init__  event with category Fast."""
        gregorian = date(2021, 6, 27)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, True)

        self.assertEqual(jewish_day.names, ['Shiva Asar BeTamuz'])

    def test__init__event_shabbat_chol_hamoed_havdala(self) -> None:
        """Test __init__ event Shabbat and Chol Hamoed."""
        # diaspora
        gregorian = date(2021, 9, 25)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, True)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, True)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(
            jewish_day.names,
            ['Shabbat', 'Chol HaMoed 3 (Sukkot 5)']
        )

        # Israel
        gregorian = date(2021, 9, 25)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, True)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, True)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(
            jewish_day.names,
            ['Shabbat', 'Chol HaMoed 4 (Sukkot 5)']
        )

    def test__init__event_shabbat_yom_tov_second_day_havdala(self) -> None:
        """Test __init__ event Shabbat and Shavuot 2."""
        # diaspora
        gregorian = date(2023, 5, 27)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, True)
        self.assertEqual(jewish_day.yom_tov, True)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Shabbat', 'Shavuot 2'])

        # Israel
        gregorian = date(2023, 5, 27)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, True)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, True)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Shabbat', 'Isru Chag'])

    def test__init__event_erev_shabbat_erev_yom_tov(self) -> None:
        """Test __init__ event Erev Shabbat and Erev Yom Tov."""
        gregorian = date(2022, 4, 15)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, True)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, False)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Erev Shabbat', 'Erev Pesach'])

    def test__init__event_shabbat__yom_tov(self) -> None:
        """Test __init__ event Shabbat and Yom Tov."""
        gregorian = date(2022, 4, 16)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, True)
        self.assertEqual(jewish_day.yom_tov, True)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, False)

        self.assertEqual(jewish_day.names, ['Shabbat', 'Pesach 1'])

    def test__init__event_yom_tov_fast(self) -> None:
        """Test __init__ event Yom Tov and Fast."""
        gregorian = date(2022, 10, 5)
        jewish_date = Date(gregorian)
        jewish_day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, jewish_day.date)

        self.assertEqual(jewish_day.erev, False)
        self.assertEqual(jewish_day.shabbat, False)
        self.assertEqual(jewish_day.yom_tov, True)
        self.assertEqual(jewish_day.chol_hamoed, False)
        self.assertEqual(jewish_day.chag, False)
        self.assertEqual(jewish_day.rosh_chodesh, False)
        self.assertEqual(jewish_day.fast, True)

        self.assertEqual(jewish_day.names, ['Yom Kippur'])

    def test__str__(self) -> None:
        """Test __str__."""
        gregorian = date(2022, 9, 1)
        jewish_day = Day(gregorian, diaspora=True)
        self.assertEqual(str(jewish_day), '5 Elul 5782 (2022-09-01)')

        # diaspora, Israel
        gregorian = date(2022, 4, 16)
        jewish_day = Day(gregorian, diaspora=True)
        self.assertEqual(
            str(jewish_day),
            '15 Nisan 5782 (2022-04-16) Shabbat, Pesach 1'
        )

        # diaspora
        gregorian = date(2022, 4, 18)
        jewish_day = Day(gregorian, diaspora=True)
        self.assertEqual(
            str(jewish_day),
            '17 Nisan 5782 (2022-04-18) Chol HaMoed 1 (Pesach 3)'
        )

        # Israel
        gregorian = date(2022, 4, 18)
        jewish_day = Day(gregorian, diaspora=False)
        self.assertEqual(
            str(jewish_day),
            '17 Nisan 5782 (2022-04-18) Chol HaMoed 2 (Pesach 3)'
        )
