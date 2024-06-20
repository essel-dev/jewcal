"""Unittests for jewcal.core."""

from datetime import date
from doctest import NORMALIZE_WHITESPACE, DocTestSuite
from typing import no_type_check
from unittest import TestCase
from unittest.mock import Mock, patch

from src.jewcal import JewCal
from src.jewcal.constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Action
from src.jewcal.models.zmanim import Location

# pylint: disable=too-many-public-methods


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

    def test_yomtov_candles(self) -> None:
        """It is a Yom Tov with a different action if Diaspora / Israel."""
        gregorian_date = date(2022, 4, 16)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.events.yomtov, YOMTOV[1][15].title)  # Pesach 1
        self.assertEqual(jewcal.events.action, Action.CANDLES.value)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.events.yomtov, YOMTOV_ISRAEL[1][15].title)  # Pesach 1
        self.assertEqual(jewcal.events.action, Action.HAVDALAH.value)

    def test_yomtov_havdalah(self) -> None:
        """It is a Yom Tov in Diaspora, Chol HaMoed in Israel."""
        gregorian_date = date(2022, 4, 17)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.events.shabbos)
        self.assertEqual(jewcal.events.yomtov, YOMTOV[1][16].title)  # Pesach 2
        self.assertEqual(jewcal.events.action, Action.HAVDALAH.value)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.events.shabbos)
        self.assertEqual(jewcal.events.yomtov, YOMTOV_ISRAEL[1][16].title)  # Ch"h 1
        self.assertIsNone(jewcal.events.action)

    def test_erev_shabbos(self) -> None:
        """It is Erev Shabbos with candles as action."""
        gregorian_date = date(2022, 8, 19)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[5].title)  # Erev Shabbos
        self.assertEqual(jewcal.events.action, Action.CANDLES.value)
        self.assertIsNone(jewcal.events.yomtov)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[5].title)  # Erev Shabbos
        self.assertEqual(jewcal.events.action, Action.CANDLES.value)
        self.assertIsNone(jewcal.events.yomtov)

    def test_shabbos(self) -> None:
        """It is Shabbos with havdalah as action."""
        gregorian_date = date(2022, 8, 20)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.events.action, Action.HAVDALAH.value)
        self.assertIsNone(jewcal.events.yomtov)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.events.action, Action.HAVDALAH.value)
        self.assertIsNone(jewcal.events.yomtov)

    def test_shabbos_chol_hamoed_sukkos(self) -> None:
        """It is Shabbos Chol Hamoed Sukkos with havdalah as action."""
        gregorian_date = date(2021, 9, 25)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.events.action, Action.HAVDALAH.value)
        self.assertEqual(jewcal.events.yomtov, YOMTOV[7][19].title)  # Ch'H Sukkos 5

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.events.action, Action.HAVDALAH.value)
        self.assertEqual(jewcal.events.yomtov, YOMTOV_ISRAEL[7][19].title)  # Sukkot 6

    def test_shabbos_chol_hamoed_pesach(self) -> None:
        """It is Shabbos Chol Hamoed Pesach with havdalah as action."""
        gregorian_date = date(2020, 4, 11)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.events.action, Action.HAVDALAH.value)
        self.assertEqual(jewcal.events.yomtov, YOMTOV[1][17].title)  # Ch'H Pesach 3

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.jewish_date.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.events.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.events.action, Action.HAVDALAH.value)
        self.assertEqual(jewcal.events.yomtov, YOMTOV_ISRAEL[1][17].title)  # Pesach 3

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

    def test_action_adjusted(self) -> None:
        """Test adjusted action."""
        # Diaspora
        # 2023
        erev_pesach = JewCal(date(2023, 4, 5))
        self.assertEqual(erev_pesach.events.action, Action.CANDLES.value)

        pesach_1 = JewCal(date(2023, 4, 6))
        self.assertEqual(pesach_1.events.action, Action.CANDLES.value)

        pesach_2 = JewCal(date(2023, 4, 7))
        self.assertEqual(pesach_2.events.action, Action.CANDLES.value)

        chol_hamoed_1 = JewCal(date(2023, 4, 8))
        self.assertEqual(chol_hamoed_1.events.action, Action.HAVDALAH.value)

        # 2024
        chol_hamoed_2 = JewCal(date(2024, 4, 26))
        self.assertEqual(chol_hamoed_2.events.action, Action.CANDLES.value)

        chol_hamoed_3 = JewCal(date(2024, 4, 27))
        self.assertEqual(chol_hamoed_3.events.action, Action.HAVDALAH.value)

        # Israel
        # 2023
        erev_pesach = JewCal(date(2023, 4, 5), diaspora=False)
        self.assertEqual(erev_pesach.events.action, Action.CANDLES.value)

        pesach_1 = JewCal(date(2023, 4, 6), diaspora=False)
        self.assertEqual(pesach_1.events.action, Action.HAVDALAH.value)

        chol_hamoed_1 = JewCal(date(2023, 4, 7), diaspora=False)
        self.assertEqual(chol_hamoed_1.events.action, Action.CANDLES.value)

        chol_hamoed_2 = JewCal(date(2023, 4, 8), diaspora=False)
        self.assertEqual(chol_hamoed_2.events.action, Action.HAVDALAH.value)

        # 2024
        chol_hamoed_3 = JewCal(date(2024, 4, 26))
        self.assertEqual(chol_hamoed_3.events.action, Action.CANDLES.value)

        chol_hamoed_4 = JewCal(date(2024, 4, 27))
        self.assertEqual(chol_hamoed_4.events.action, Action.HAVDALAH.value)

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

    @patch('src.jewcal.core.date_today', autospec=True)
    def test_hadlokas_haneiros_is_set(self, mock_today: Mock) -> None:
        """Test Hadlokas Haneiros is set."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        date_ = date(2024, 5, 31)  # erev shabbos
        mock_today.return_value = date_
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNotNone(jewcal.zmanim.hadlokas_haneiros)

    @patch('src.jewcal.core.date_today', autospec=True)
    def test_hadlokas_haneiros_is_not_set(self, mock_today: Mock) -> None:
        """Test Hadlokas Haneiros is not set."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        date_ = date(2024, 6, 1)  # shabbos
        mock_today.return_value = date_
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNone(jewcal.zmanim.hadlokas_haneiros)

        date_ = date(2024, 6, 2)  # sunday
        mock_today.return_value = date_
        jewcal = JewCal(date_, location)
        if not jewcal.zmanim:
            raise TypeError
        self.assertIsNone(jewcal.zmanim.hadlokas_haneiros)
