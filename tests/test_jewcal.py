"""Unittests for jewcal."""

from datetime import date
from unittest import TestCase

from src.jewcal import Jewcal
from src.jewcal.constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Category


class JewcalTestCase(TestCase):
    """Unittests for jewcal."""

    def setUp(self) -> None:
        """Initialize."""

    def tearDown(self) -> None:
        """Clean up after tests."""

    def test_no_shabbos_and_yom_tov(self) -> None:
        """Create a new date."""
        gregorian_date = date(2022, 8, 14)

        # Diaspora
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertIsNone(jewcal.yomtov)
        self.assertIsNone(jewcal.category)

        # Israel
        jewcal = Jewcal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertIsNone(jewcal.yomtov)
        self.assertIsNone(jewcal.category)

    def test_yomtov_candles(self) -> None:
        """It is a Yom Tov with a different category if Diaspora / Israel."""
        gregorian_date = date(2022, 4, 16)

        # Diaspora
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.yomtov, YOMTOV[1][15].title)  # Pesach 1
        self.assertEqual(jewcal.category, Category.CANDLES.value)

        # Israel
        jewcal = Jewcal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.yomtov, YOMTOV_ISRAEL[1][15].title)  # Pesach 1
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)

    def test_yomtov_havdalah(self) -> None:
        """It is a Yom Tov in Diaspora, Chol HaMoed in Israel."""
        gregorian_date = date(2022, 4, 17)

        # Diaspora
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertEqual(jewcal.yomtov, YOMTOV[1][16].title)  # Pesach 2
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)

        # Israel
        jewcal = Jewcal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertEqual(jewcal.yomtov, YOMTOV_ISRAEL[1][16].title)  # Ch"h 1
        self.assertIsNone(jewcal.category)

    def test_erev_shabbos(self) -> None:
        """It is Erev Shabbos with candles as category."""
        gregorian_date = date(2022, 8, 19)

        # Diaspora
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[5].title)  # Erev Shabbos
        self.assertEqual(jewcal.category, Category.CANDLES.value)
        self.assertIsNone(jewcal.yomtov)

        # Israel
        jewcal = Jewcal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[5].title)  # Erev Shabbos
        self.assertEqual(jewcal.category, Category.CANDLES.value)
        self.assertIsNone(jewcal.yomtov)

    def test_shabbos(self) -> None:
        """It is Shabbos with havdalah as category."""
        gregorian_date = date(2022, 8, 20)

        # Diaspora
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertIsNone(jewcal.yomtov)

        # Israel
        jewcal = Jewcal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertIsNone(jewcal.yomtov)

    def test_shabbos_chol_hamoed_sukkos(self) -> None:
        """It is Shabbos Chol Hamoed Sukkos with havdalah as category."""
        gregorian_date = date(2021, 9, 25)

        # Diaspora
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV[7][19].title)  # Ch'H Sukkos 5

        # Israel
        jewcal = Jewcal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV_ISRAEL[7][19].title)  # Sukkot 6

    def test_shabbos_chol_hamoed_pesach(self) -> None:
        """It is Shabbos Chol Hamoed Pesach with havdalah as category."""
        gregorian_date = date(2020, 4, 11)

        # Diaspora
        jewcal = Jewcal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV[1][17].title)  # Ch'H Pesach 3

        # Israel
        jewcal = Jewcal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV_ISRAEL[1][17].title)  # Pesach 3

    def test_jewcal_to_string(self) -> None:
        """Test `Jewcal`-object to `str`."""
        jewcal = Jewcal(date(2022, 4, 16))
        self.assertEqual(str(jewcal), '15 Nisan 5782')

    def test_jewcal_to_repr(self) -> None:
        """Test `Jewcal`-object to `repr`."""
        # Diaspora
        jewcal = Jewcal(date(2022, 4, 16))
        self.assertEqual(
            repr(jewcal),
            'Jewcal(year=5782, month=1, day=15, '
            + "gregorian_date=datetime.date(2022, 4, 16), shabbos='Shabbos', "
            + "yomtov='Pesach 1', category='Candles', diaspora=True)"
        )

        # Israel
        jewcal = Jewcal(date(2022, 4, 16), diaspora=False)
        self.assertEqual(
            repr(jewcal),
            'Jewcal(year=5782, month=1, day=15, '
            + 'gregorian_date=datetime.date(2022, 4, 16), '
            + "shabbos='Shabbos', yomtov='Pesach 1', category='Havdalah', "
            + 'diaspora=False)'
        )
