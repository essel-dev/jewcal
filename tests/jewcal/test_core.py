"""Unittests for jewcal.core."""

from datetime import date, datetime, timezone
from doctest import NORMALIZE_WHITESPACE, DocTestSuite
from typing import no_type_check
from unittest import TestCase
from unittest.mock import Mock, patch

from src.jewcal import JewCal
from src.jewcal.constants import SHABBOS, Action
from src.jewcal.models.zmanim import Location


@no_type_check
# pylint: disable=unused-argument
def load_tests(loader, tests, ignore):  # noqa: ANN201, ANN001, ARG001
    """Run the doctests in jewcal.core for documentation (tutorials).

    # noqa: DAR101 loader
    # noqa: DAR101 tests
    # noqa: DAR101 ignore
    # noqa: DAR201 return
    """
    tests.addTests(DocTestSuite('src.jewcal.core', optionflags=NORMALIZE_WHITESPACE))
    return tests


class JewCalTestCase(TestCase):
    """Unittests for JewCal."""

    def setUp(self) -> None:
        """Initialize."""

    def tearDown(self) -> None:
        """Clean up after tests."""

    def test_deprecated_class_name(self) -> None:
        """Using the old class name should alert the user."""
        with self.assertWarns(UserWarning):
            # pylint: disable=import-outside-toplevel,unused-import
            from src.jewcal import Jewcal

            Jewcal(date(2022, 8, 14))

    def test_no_shabbos_and_yomtov(self) -> None:
        """Create a new date."""
        gregorian_date = date(2022, 8, 14)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertTrue(jewcal.diaspora)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.events.shabbos)
        self.assertIsNone(jewcal.events.yomtov)
        self.assertIsNone(jewcal.events.action)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.events.shabbos)
        self.assertIsNone(jewcal.events.yomtov)
        self.assertIsNone(jewcal.events.action)

    def test_jewcal_to_string(self) -> None:
        """Test `JewCal`-object to `str`."""
        # non-leap Jewish year
        jewcal = JewCal(date(2023, 3, 15))
        self.assertEqual(str(jewcal), '22 Adar 5783')

        # leap Jewish year
        jewcal = JewCal(date(2022, 4, 16))
        self.assertEqual(str(jewcal), '15 Nisan 5782: Shabbos, Pesach 1')

        jewcal = JewCal(date(2022, 2, 27))
        self.assertEqual(str(jewcal), '26 Adar 1 5782')

        jewcal = JewCal(date(2022, 3, 16))
        self.assertEqual(str(jewcal), '13 Adar 2 5782')

        jewcal = JewCal(date(2024, 2, 10))
        self.assertEqual(str(jewcal), '1 Adar 1 5784: Shabbos')

        jewcal = JewCal(date(2024, 3, 11))
        self.assertEqual(str(jewcal), '1 Adar 2 5784')

    def test_jewcal_to_repr(self) -> None:
        """Test `JewCal`-object to `repr`."""
        jewcal = JewCal(date(2022, 4, 16))
        self.assertEqual(
            repr(jewcal),
            (
                'JewCal(jewish_date=JewishDate(year=5782, month=1, day=15, '
                'gregorian_date=datetime.date(2022, 4, 16)), '
                "events=Events(shabbos='Shabbos', yomtov='Pesach 1', "
                "action='Candles'), diaspora=True, zmanim=None)"
            ),
        )

        # Israel
        jewcal = JewCal(date(2022, 4, 16), diaspora=False)
        self.assertEqual(
            repr(jewcal),
            (
                'JewCal(jewish_date=JewishDate(year=5782, month=1, day=15, '
                'gregorian_date=datetime.date(2022, 4, 16)), '
                "events=Events(shabbos='Shabbos', yomtov='Pesach 1', "
                "action='Havdalah'), diaspora=False, zmanim=None)"
            ),
        )

    def test_deprecated_jewish_date_attributes(self) -> None:
        """Test deprecated jewish date attributes."""
        jewcal = JewCal(date(2024, 6, 14))

        with self.assertWarns(Warning):
            self.assertIsNotNone(jewcal.year)
            self.assertEqual(jewcal.year, 5784)

        with self.assertWarns(Warning):
            self.assertIsNotNone(jewcal.month)
            self.assertEqual(jewcal.month, 3)

        with self.assertWarns(Warning):
            self.assertIsNotNone(jewcal.day)
            self.assertEqual(jewcal.day, 8)

        with self.assertWarns(Warning):
            self.assertIsNotNone(jewcal.gregorian_date)
            self.assertEqual(jewcal.gregorian_date, date(2024, 6, 14))

    def test_deprecated_events_attributes(self) -> None:
        """Test deprecated events attributes."""
        jewcal = JewCal(date(2024, 6, 14))

        with self.assertWarns(Warning):
            self.assertEqual(jewcal.shabbos, SHABBOS[5].title)

        with self.assertWarns(Warning):
            self.assertIsNone(jewcal.yomtov)

        with self.assertWarns(Warning):
            self.assertEqual(jewcal.category, Action.CANDLES.value)

    def test_events_methods_exists(self) -> None:
        """Test `Events` methods are accessible in `JewCal` class."""
        jewcal = JewCal()

        self.assertIsNotNone(jewcal.has_events())
        self.assertIsNotNone(jewcal.is_erev_shabbos())
        self.assertIsNotNone(jewcal.is_shabbos())
        self.assertIsNotNone(jewcal.is_erev_yomtov())
        self.assertIsNotNone(jewcal.is_yomtov())
        self.assertIsNotNone(jewcal.is_erev())
        self.assertIsNotNone(jewcal.is_issur_melacha())

    def test_zmanim_property_exists(self) -> None:
        """Test `Zmanim` property exists."""
        jewcal = JewCal()
        self.assertIsNone(jewcal.zmanim)

    def test_zmanim_init(self) -> None:
        """Test Zmanim init."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        jewcal = JewCal(location=Location(latitude=lat, longitude=lon))
        self.assertIsNotNone(jewcal.zmanim)

    def test_zmanim_init_fail(self) -> None:
        """Zmanim should be `None` when no `Location` is given."""
        jewcal = JewCal()
        self.assertIsNone(jewcal.zmanim)

    @patch('src.jewcal.core.date_today', autospec=True)
    @patch('src.jewcal.core.Zmanim.is_now_after_nightfall', autospec=True)
    def test_is_now_after_nightfall_true(
        self,
        mock_zmanim: Mock,
        mock_today: Mock,
    ) -> None:
        """Test Gregorian date should be next day."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        date_ = date(2024, 5, 31)
        mock_today.return_value = date_
        mock_zmanim.return_value = True
        jewcal = JewCal(date_, location)
        self.assertEqual(jewcal.jewish_date.gregorian_date, date(2024, 6, 1))

    @patch('src.jewcal.core.date_today', autospec=True)
    @patch('src.jewcal.core.Zmanim.is_now_after_nightfall', autospec=True)
    def test_is_now_after_nightfall_false(
        self,
        mock_zmanim: Mock,
        mock_today: Mock,
    ) -> None:
        """Test Gregorian date remains the same."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        date_ = date(2024, 5, 31)
        mock_today.return_value = date_
        mock_zmanim.return_value = False
        jewcal = JewCal(date_, location)
        self.assertEqual(jewcal.jewish_date.gregorian_date, date_)

    def test_hadlokas_haneiros_is_set(self) -> None:
        """Test Hadlokas Haneiros is set."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        date_ = date(2024, 5, 31)  # erev shabbos
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNotNone(jewcal.zmanim.hadlokas_haneiros)

    @patch('src.jewcal.models.zmanim.datetime_now', autospec=True)
    @patch('src.jewcal.models.zmanim.date_today', autospec=True)
    @patch('src.jewcal.core.date_today', autospec=True)
    def test_hadlokas_haneiros_is_set_and_after_nightfall(
        self,
        mock_core_today: Mock,
        mock_today: Mock,
        mock_now: Mock,
    ) -> None:
        """Test has Hadlokas Haneiros, is after nightfall, has next Gregorian date."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        date_ = date(2024, 7, 25)
        now_ = datetime(2024, 7, 25, 20, 42, tzinfo=timezone.utc)
        mock_core_today.return_value = date_
        mock_today.return_value = date_
        mock_now.return_value = now_
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError

        self.assertIsNotNone(jewcal.zmanim.hadlokas_haneiros)

    def test_hadlokas_haneiros_is_set_second_day_yom_tov(self) -> None:
        """Test has Hadlokas Haneiros for second day of Yom Tov."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        date_ = date(2024, 6, 11)  # Erev Shavuos
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNotNone(jewcal.zmanim.hadlokas_haneiros)

        date_ = date(2024, 6, 12)  # Shavuos 1
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNotNone(jewcal.zmanim.hadlokas_haneiros)

        date_ = date(2024, 6, 13)  # Shavuos 2
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNone(jewcal.zmanim.hadlokas_haneiros)

        date_ = date(2024, 6, 14)  # Erev Shabbos
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNotNone(jewcal.zmanim.hadlokas_haneiros)

        date_ = date(2024, 6, 15)  # Shabbos
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNone(jewcal.zmanim.hadlokas_haneiros)

    def test_hadlokas_haneiros_is_not_set(self) -> None:
        """Test Hadlokas Haneiros is not set."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        date_ = date(2024, 6, 1)  # shabbos
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNone(jewcal.zmanim.hadlokas_haneiros)

        date_ = date(2024, 6, 2)  # sunday
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNone(jewcal.zmanim.hadlokas_haneiros)
