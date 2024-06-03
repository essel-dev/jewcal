"""Unittests for jewcal."""

from datetime import date
from unittest import TestCase

from src.jewcal import JewCal
from src.jewcal.constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Category


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

    def test_no_shabbos_and_yom_tov(self) -> None:
        """Create a new date."""
        gregorian_date = date(2022, 8, 14)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertIsNone(jewcal.yomtov)
        self.assertIsNone(jewcal.category)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertIsNone(jewcal.yomtov)
        self.assertIsNone(jewcal.category)

    def test_yomtov_candles(self) -> None:
        """It is a Yom Tov with a different category if Diaspora / Israel."""
        gregorian_date = date(2022, 4, 16)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.yomtov, YOMTOV[1][15].title)  # Pesach 1
        self.assertEqual(jewcal.category, Category.CANDLES.value)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.yomtov, YOMTOV_ISRAEL[1][15].title)  # Pesach 1
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)

    def test_yomtov_havdalah(self) -> None:
        """It is a Yom Tov in Diaspora, Chol HaMoed in Israel."""
        gregorian_date = date(2022, 4, 17)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertEqual(jewcal.yomtov, YOMTOV[1][16].title)  # Pesach 2
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertIsNone(jewcal.shabbos)
        self.assertEqual(jewcal.yomtov, YOMTOV_ISRAEL[1][16].title)  # Ch"h 1
        self.assertIsNone(jewcal.category)

    def test_erev_shabbos(self) -> None:
        """It is Erev Shabbos with candles as category."""
        gregorian_date = date(2022, 8, 19)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[5].title)  # Erev Shabbos
        self.assertEqual(jewcal.category, Category.CANDLES.value)
        self.assertIsNone(jewcal.yomtov)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[5].title)  # Erev Shabbos
        self.assertEqual(jewcal.category, Category.CANDLES.value)
        self.assertIsNone(jewcal.yomtov)

    def test_shabbos(self) -> None:
        """It is Shabbos with havdalah as category."""
        gregorian_date = date(2022, 8, 20)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertIsNone(jewcal.yomtov)

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertIsNone(jewcal.yomtov)

    def test_shabbos_chol_hamoed_sukkos(self) -> None:
        """It is Shabbos Chol Hamoed Sukkos with havdalah as category."""
        gregorian_date = date(2021, 9, 25)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV[7][19].title)  # Ch'H Sukkos 5

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV_ISRAEL[7][19].title)  # Sukkot 6

    def test_shabbos_chol_hamoed_pesach(self) -> None:
        """It is Shabbos Chol Hamoed Pesach with havdalah as category."""
        gregorian_date = date(2020, 4, 11)

        # Diaspora
        jewcal = JewCal(gregorian_date)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV[1][17].title)  # Ch'H Pesach 3

        # Israel
        jewcal = JewCal(gregorian_date, diaspora=False)

        self.assertEqual(jewcal.gregorian_date, gregorian_date)

        self.assertEqual(jewcal.shabbos, SHABBOS[6].title)  # Shabbos
        self.assertEqual(jewcal.category, Category.HAVDALAH.value)
        self.assertEqual(jewcal.yomtov, YOMTOV_ISRAEL[1][17].title)  # Pesach 3

    def test_jewcal_to_string(self) -> None:
        """Test `JewCal`-object to `str`."""
        jewcal = JewCal(date(2022, 4, 16))
        self.assertEqual(str(jewcal), '15 Nisan 5782')

    def test_jewcal_to_repr(self) -> None:
        """Test `JewCal`-object to `repr`."""
        # Diaspora
        jewcal = JewCal(date(2022, 4, 16))
        self.assertEqual(
            repr(jewcal),
            'JewCal(year=5782, month=1, day=15, '
            + "gregorian_date=datetime.date(2022, 4, 16), shabbos='Shabbos', "
            + "yomtov='Pesach 1', category='Candles', is_erev=False, diaspora=True)",
        )

        # Israel
        jewcal = JewCal(date(2022, 4, 16), diaspora=False)
        self.assertEqual(
            repr(jewcal),
            'JewCal(year=5782, month=1, day=15, '
            + 'gregorian_date=datetime.date(2022, 4, 16), '
            + "shabbos='Shabbos', yomtov='Pesach 1', category='Havdalah', "
            + 'is_erev=False, diaspora=False)',
        )

    def test_category_adjusted(self) -> None:
        """Test adjusted category."""
        # Diaspora
        # 2023
        erev_pesach = JewCal(date(2023, 4, 5))
        self.assertEqual(erev_pesach.category, Category.CANDLES.value)

        pesach_1 = JewCal(date(2023, 4, 6))
        self.assertEqual(pesach_1.category, Category.CANDLES.value)

        pesach_2 = JewCal(date(2023, 4, 7))
        self.assertEqual(pesach_2.category, Category.CANDLES.value)

        chol_hamoed_1 = JewCal(date(2023, 4, 8))
        self.assertEqual(chol_hamoed_1.category, Category.HAVDALAH.value)

        # 2024
        chol_hamoed_2 = JewCal(date(2024, 4, 26))
        self.assertEqual(chol_hamoed_2.category, Category.CANDLES.value)

        chol_hamoed_3 = JewCal(date(2024, 4, 27))
        self.assertEqual(chol_hamoed_3.category, Category.HAVDALAH.value)

        # Israel
        # 2023
        erev_pesach = JewCal(date(2023, 4, 5), diaspora=False)
        self.assertEqual(erev_pesach.category, Category.CANDLES.value)

        pesach_1 = JewCal(date(2023, 4, 6), diaspora=False)
        self.assertEqual(pesach_1.category, Category.HAVDALAH.value)

        chol_hamoed_1 = JewCal(date(2023, 4, 7), diaspora=False)
        self.assertEqual(chol_hamoed_1.category, Category.CANDLES.value)

        chol_hamoed_2 = JewCal(date(2023, 4, 8), diaspora=False)
        self.assertEqual(chol_hamoed_2.category, Category.HAVDALAH.value)

        # 2024
        chol_hamoed_3 = JewCal(date(2024, 4, 26))
        self.assertEqual(chol_hamoed_3.category, Category.CANDLES.value)

        chol_hamoed_4 = JewCal(date(2024, 4, 27))
        self.assertEqual(chol_hamoed_4.category, Category.HAVDALAH.value)

    def test_erev(self) -> None:
        """Test Erev Shabbos and Yom Tov."""
        # Shabbos
        erev_shabbos_1 = JewCal(date(2023, 9, 15))
        self.assertTrue(erev_shabbos_1.is_erev)

        shabbos_1 = JewCal(date(2023, 9, 16))
        self.assertFalse(shabbos_1.is_erev)

        sunday = JewCal(date(2023, 9, 17))
        self.assertFalse(sunday.is_erev)

        erev_shabbos_2 = JewCal(date(2023, 9, 22), diaspora=False)
        self.assertTrue(erev_shabbos_2.is_erev)

        shabbos_2 = JewCal(date(2023, 9, 23), diaspora=False)
        self.assertFalse(shabbos_2.is_erev)

        # Diaspora
        erev_pesach = JewCal(date(2024, 4, 22))
        self.assertTrue(erev_pesach.is_erev)

        pesach_1 = JewCal(date(2024, 4, 23))
        self.assertFalse(pesach_1.is_erev)

        pesach_2 = JewCal(date(2024, 4, 24))
        self.assertFalse(pesach_2.is_erev)

        chol_hamoed_1 = JewCal(date(2024, 4, 25))
        self.assertFalse(chol_hamoed_1.is_erev)

        chol_hamoed_2 = JewCal(date(2024, 4, 26))
        self.assertTrue(chol_hamoed_2.is_erev)  # erev shabbos Chol HaMoed 2 (Pesach 4)

        chol_hamoed_3 = JewCal(date(2024, 4, 27))
        self.assertFalse(chol_hamoed_3.is_erev)  # shabbos

        # Israel
        erev_pesach = JewCal(date(2024, 4, 22), diaspora=False)
        self.assertTrue(erev_pesach.is_erev)

        pesach_1 = JewCal(date(2024, 4, 23), diaspora=False)
        self.assertFalse(pesach_1.is_erev)

        chol_hamoed_1 = JewCal(date(2024, 4, 24), diaspora=False)
        self.assertFalse(chol_hamoed_1.is_erev)

        chol_hamoed_2 = JewCal(date(2024, 4, 26), diaspora=False)
        self.assertTrue(chol_hamoed_2.is_erev)  # erev shabbos Chol HaMoed 2 (Pesach 3)

        chol_hamoed_3 = JewCal(date(2024, 4, 27), diaspora=False)
        self.assertFalse(chol_hamoed_3.is_erev)  # shabbos

        # Diaspora
        erev_rosh_hashana = JewCal(date(2024, 10, 2))
        self.assertTrue(erev_rosh_hashana.is_erev)

        rosh_hashana_1 = JewCal(date(2024, 10, 3))
        self.assertFalse(rosh_hashana_1.is_erev)

        rosh_hashana_2 = JewCal(date(2024, 10, 4))  # Friday
        self.assertFalse(rosh_hashana_2.is_erev)

        shabbos = JewCal(date(2024, 10, 5))
        self.assertFalse(shabbos.is_erev)

        # Israel
        erev_rosh_hashana = JewCal(date(2024, 10, 2), diaspora=False)
        self.assertTrue(erev_rosh_hashana.is_erev)

        rosh_hashana_1 = JewCal(date(2024, 10, 3), diaspora=False)
        self.assertFalse(rosh_hashana_1.is_erev)

        rosh_hashana_2 = JewCal(date(2024, 10, 4), diaspora=False)  # Friday
        self.assertFalse(rosh_hashana_2.is_erev)

        shabbos = JewCal(date(2024, 10, 5), diaspora=False)
        self.assertFalse(shabbos.is_erev)
