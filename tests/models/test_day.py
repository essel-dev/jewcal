"""Unittests for jewcal.models.day."""

from datetime import date
from unittest import TestCase

from src.jewcal.models.date import Date
from src.jewcal.models.day import Day


class DayTestCase(TestCase):
    """Unittests for `Day`."""

    def test_has_no_event(self) -> None:
        """Test no event and no category."""
        gregorian = date(2022, 9, 1)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, False)

        self.assertFalse(day.names)

        self.assertFalse(day.active_categories())
        self.assertEqual(day.is_holiday(), False)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), False)
        self.assertEqual(day.is_chag(), False)

    def test_event_category_erev(self) -> None:
        """Test event with category Erev."""
        gregorian = date(2022, 9, 25)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, True)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Erev Rosh Hashana'])

        self.assertEqual(day.active_categories(), ['erev_yomtov'])
        self.assertEqual(day.is_holiday(), False)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), True)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), False)
        self.assertEqual(day.is_chag(), False)

    def test_event_category_shabbat(self) -> None:
        """Test event with category Shabbat."""
        gregorian = date(2022, 9, 3)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Shabbat'])

        self.assertEqual(day.active_categories(), ['shabbat'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), True)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), False)

    def test_event_category_yomtov(self) -> None:
        """Test event with category Yom Tov."""
        gregorian = date(2022, 9, 27)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Rosh Hashana 2'])

        self.assertEqual(day.active_categories(), ['yomtov'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), True)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), False)

    def test_event_category_chag_chol_hamoed(self) -> None:
        """Test event with category Chag for Chol HaMoed."""
        # diaspora
        gregorian = date(2022, 4, 18)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Pesach Chol HaMoed 1'])

        self.assertEqual(day.active_categories(), ['chag'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), False)
        self.assertEqual(day.is_chag(), True)

        # Israel
        gregorian = date(2022, 4, 18)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Pesach Chol HaMoed 2'])

        self.assertEqual(day.active_categories(), ['chag'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), False)
        self.assertEqual(day.is_chag(), True)

    def test_event_category_erev_shmini_atzeret(self) -> None:
        """Test event with category Hoshana Raba and Erev Yom Tov."""
        # diaspora
        gregorian = date(2022, 10, 16)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, True)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Hoshana Raba'])

        self.assertEqual(day.active_categories(), ['erev_yomtov', 'chag'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), True)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), False)
        self.assertEqual(day.is_chag(), True)

    def test_event_category_chag(self) -> None:
        """Test event with category Chag."""
        gregorian = date(2022, 12, 19)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Chanuka 1'])

        self.assertEqual(day.active_categories(), ['chag'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), False)
        self.assertEqual(day.is_chag(), True)

    def test_event_category_fast(self) -> None:
        """Test event with category Fast."""
        gregorian = date(2021, 6, 27)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, True)

        self.assertEqual(day.names, ['Shiva Asar BeTamuz'])

        self.assertEqual(day.active_categories(), ['fast'])
        self.assertEqual(day.is_holiday(), False)
        self.assertEqual(day.is_fast_day(), True)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), False)
        self.assertEqual(day.is_chag(), False)

    def test_event_shabbat_chol_hamoed(self) -> None:
        """Test event Shabbat and Chol HaMoed."""
        # diaspora
        gregorian = date(2021, 9, 25)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(
            day.names,
            ['Shabbat', 'Sukkot Chol HaMoed 3']
        )

        self.assertEqual(day.active_categories(), ['shabbat', 'chag'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), True)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), True)

        # Israel
        gregorian = date(2021, 9, 25)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(
            day.names,
            ['Shabbat', 'Sukkot Chol HaMoed 4']
        )

        self.assertEqual(day.active_categories(), ['shabbat', 'chag'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), True)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), True)

    def test_event_shabbat_yomtov_second_day(self) -> None:
        """Test event Shabbat and Shavuot 2."""
        # diaspora
        gregorian = date(2023, 5, 27)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Shabbat', 'Shavuot 2'])

        self.assertEqual(day.active_categories(), ['shabbat', 'yomtov'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), True)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), True)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), False)

        # Israel
        gregorian = date(2023, 5, 27)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=False)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Shabbat', 'Isru Chag'])

        self.assertEqual(day.active_categories(), ['shabbat', 'chag'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), True)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), True)

    def test_event_erev_shabbat_erev_yomtov(self) -> None:
        """Test event Erev Shabbat and Erev Yom Tov."""
        gregorian = date(2022, 4, 15)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, True)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, True)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Erev Shabbat', 'Erev Pesach'])

        self.assertEqual(
            day.active_categories(),
            ['erev_shabbat', 'erev_yomtov']
        )
        self.assertEqual(day.is_holiday(), False)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), True)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), True)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), False)
        self.assertEqual(day.is_chag(), False)

    def test_event_shabbat_yomtov(self) -> None:
        """Test event Shabbat and Yom Tov."""
        gregorian = date(2022, 4, 16)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(day.names, ['Shabbat', 'Pesach 1'])

        self.assertEqual(day.active_categories(), ['shabbat', 'yomtov'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), True)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), True)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), False)

    def test_event_yomtov_fast(self) -> None:
        """Test event Yom Tov and Fast."""
        # Not on Shabbat
        gregorian = date(2022, 10, 5)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, False)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, True)

        self.assertEqual(day.names, ['Yom Kippur'])

        self.assertEqual(day.active_categories(), ['yomtov', 'fast'])
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), True)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), False)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), True)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), False)

        # On Shabbat
        gregorian = date(2024, 10, 12)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, True)
        self.assertEqual(day.categories.chag, False)
        self.assertEqual(day.categories.fast, True)

        self.assertEqual(day.names, ['Shabbat', 'Yom Kippur'])

        self.assertEqual(
            day.active_categories(), ['shabbat', 'yomtov', 'fast']
        )
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), True)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), True)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), True)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), False)

    def test_event_rosh_chodesh_chanuka(self) -> None:
        """Test event Rosh Chodesh Teves and Chanuka 6."""
        gregorian = date(2022, 12, 24)
        jewish_date = Date(gregorian)
        day = Day(gregorian, diaspora=True)

        self.assertEqual(jewish_date, day.date)

        self.assertEqual(day.categories.erev_shabbat, False)
        self.assertEqual(day.categories.shabbat, True)
        self.assertEqual(day.categories.erev_yomtov, False)
        self.assertEqual(day.categories.yomtov, False)
        self.assertEqual(day.categories.chag, True)
        self.assertEqual(day.categories.fast, False)

        self.assertEqual(
            day.names,
            ['Shabbat', 'Chanuka 6', 'Rosh Chodesh Tevet']
        )

        self.assertEqual(
            day.active_categories(),
            ['shabbat', 'chag']
        )
        self.assertEqual(day.is_holiday(), True)
        self.assertEqual(day.is_fast_day(), False)
        self.assertEqual(day.is_erev_shabbat(), False)
        self.assertEqual(day.is_shabbat(), True)
        self.assertEqual(day.is_erev_yomtov(), False)
        self.assertEqual(day.is_yomtov(), False)
        self.assertEqual(day.is_issur_melacha(), True)
        self.assertEqual(day.is_chag(), True)

    def test__str__(self) -> None:
        """Test __str__."""
        gregorian = date(2022, 9, 1)
        day = Day(gregorian, diaspora=True)
        self.assertEqual(str(day), '5 Elul 5782 (2022-09-01)')

        # diaspora, Israel
        gregorian = date(2022, 4, 16)
        day = Day(gregorian, diaspora=True)
        self.assertEqual(
            str(day), '15 Nisan 5782 (2022-04-16) Shabbat, Pesach 1'
        )

        # diaspora
        gregorian = date(2022, 4, 18)
        day = Day(gregorian, diaspora=True)
        self.assertEqual(
            str(day), '17 Nisan 5782 (2022-04-18) Pesach Chol HaMoed 1'
        )

        # Israel
        gregorian = date(2022, 4, 18)
        day = Day(gregorian, diaspora=False)
        self.assertEqual(
            str(day), '17 Nisan 5782 (2022-04-18) Pesach Chol HaMoed 2'
        )
