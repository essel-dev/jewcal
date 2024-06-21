"""Unittests for jewcal.models.events."""

from unittest import TestCase

from src.jewcal.constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL, Action
from src.jewcal.models.events import Events

# ruff: noqa: SLF001
# pylint: disable=W0212


class EventsTestCase(TestCase):
    """Unittests for Events."""

    def test_attr_yomtov(self) -> None:
        """It is a Yom Tov with a different action if Diaspora / Israel."""
        # Diaspora
        # 2022, 4, 16
        shabbos_pesach_1 = Events(6, 1, 15, diaspora=True)
        self.assertEqual(shabbos_pesach_1.shabbos, SHABBOS[6].title)
        self.assertEqual(shabbos_pesach_1.yomtov, YOMTOV[1][15].title)
        self.assertEqual(shabbos_pesach_1.action, Action.CANDLES.value)

        # 2022, 4, 17
        pesach_2 = Events(0, 1, 16, diaspora=True)
        self.assertIsNone(pesach_2.shabbos)
        self.assertEqual(pesach_2.yomtov, YOMTOV[1][16].title)
        self.assertEqual(pesach_2.action, Action.HAVDALAH.value)

        # Israel
        # 2022, 4, 16
        shabbos_pesach_1 = Events(6, 1, 15, diaspora=False)
        self.assertEqual(shabbos_pesach_1.shabbos, SHABBOS[6].title)
        self.assertEqual(shabbos_pesach_1.yomtov, YOMTOV_ISRAEL[1][15].title)
        self.assertEqual(shabbos_pesach_1.action, Action.HAVDALAH.value)

        # 2022, 4, 17
        ch_h_pesach_2 = Events(0, 1, 16, diaspora=False)
        self.assertIsNone(ch_h_pesach_2.shabbos)
        self.assertEqual(ch_h_pesach_2.yomtov, YOMTOV_ISRAEL[1][16].title)
        self.assertIsNone(ch_h_pesach_2.action)

    def test_attr_erev_shabbos(self) -> None:
        """It is Erev Shabbos with candles as action."""
        # 2024-06-21

        # Diaspora
        erev_shabbos = Events(5, 3, 15, diaspora=True)
        self.assertEqual(erev_shabbos.shabbos, SHABBOS[5].title)
        self.assertEqual(erev_shabbos.action, Action.CANDLES.value)
        self.assertIsNone(erev_shabbos.yomtov)

        # Israel
        erev_shabbos = Events(5, 3, 15, diaspora=False)
        self.assertEqual(erev_shabbos.shabbos, SHABBOS[5].title)
        self.assertEqual(erev_shabbos.action, Action.CANDLES.value)
        self.assertIsNone(erev_shabbos.yomtov)

    def test_attr_shabbos(self) -> None:
        """It is Shabbos with havdalah as action."""
        # 2024-06-22

        # Diaspora
        shabbos = Events(6, 3, 16, diaspora=True)
        self.assertEqual(shabbos.shabbos, SHABBOS[6].title)
        self.assertEqual(shabbos.action, Action.HAVDALAH.value)
        self.assertIsNone(shabbos.yomtov)

        # Israel
        shabbos = Events(6, 3, 16, diaspora=False)
        self.assertEqual(shabbos.shabbos, SHABBOS[6].title)
        self.assertEqual(shabbos.action, Action.HAVDALAH.value)
        self.assertIsNone(shabbos.yomtov)

    def test_attr_shabbos_chol_hamoed_sukkos(self) -> None:
        """It is Shabbos Chol Hamoed Sukkos with havdalah as action."""
        # 2021, 9, 25

        # Diaspora
        shabbos_ch_h_sukkos = Events(6, 7, 19, diaspora=True)
        self.assertEqual(shabbos_ch_h_sukkos.shabbos, SHABBOS[6].title)
        self.assertEqual(shabbos_ch_h_sukkos.action, Action.HAVDALAH.value)
        self.assertEqual(shabbos_ch_h_sukkos.yomtov, YOMTOV[7][19].title)

        # Israel
        shabbos_ch_h_sukkos = Events(6, 7, 19, diaspora=False)
        self.assertEqual(shabbos_ch_h_sukkos.shabbos, SHABBOS[6].title)
        self.assertEqual(shabbos_ch_h_sukkos.action, Action.HAVDALAH.value)
        self.assertEqual(shabbos_ch_h_sukkos.yomtov, YOMTOV_ISRAEL[7][19].title)

    def test_attr_shabbos_chol_hamoed_pesach(self) -> None:
        """It is Shabbos Chol Hamoed Pesach with havdalah as action."""
        # 2020, 4, 11

        # Diaspora
        shabbos_ch_h_pesach = Events(6, 1, 17, diaspora=True)
        self.assertEqual(shabbos_ch_h_pesach.shabbos, SHABBOS[6].title)
        self.assertEqual(shabbos_ch_h_pesach.action, Action.HAVDALAH.value)
        self.assertEqual(shabbos_ch_h_pesach.yomtov, YOMTOV[1][17].title)

        # Israel
        shabbos_ch_h_pesach = Events(6, 1, 17, diaspora=False)
        self.assertEqual(shabbos_ch_h_pesach.shabbos, SHABBOS[6].title)
        self.assertEqual(shabbos_ch_h_pesach.action, Action.HAVDALAH.value)
        self.assertEqual(shabbos_ch_h_pesach.yomtov, YOMTOV_ISRAEL[1][17].title)

    def test_action_adjusted(self) -> None:
        """Test adjusted action."""
        # Diaspora
        # 2023
        erev_pesach = Events(3, 1, 14, diaspora=True)  # 2023, 4, 5
        self.assertEqual(erev_pesach.action, Action.CANDLES.value)

        pesach_1 = Events(4, 1, 15, diaspora=True)  # 2023, 4, 6
        self.assertEqual(pesach_1.action, Action.CANDLES.value)

        pesach_2 = Events(5, 1, 16, diaspora=True)  # 2023, 4, 7
        self.assertEqual(pesach_2.action, Action.CANDLES.value)

        chol_hamoed_1 = Events(6, 1, 17, diaspora=True)  # 2023, 4, 8
        self.assertEqual(chol_hamoed_1.action, Action.HAVDALAH.value)

        # 2024
        chol_hamoed_2 = Events(5, 1, 18, diaspora=True)  # 2024, 4, 26
        self.assertEqual(chol_hamoed_2.action, Action.CANDLES.value)

        chol_hamoed_3 = Events(6, 1, 19, diaspora=True)  # 2024, 4, 27
        self.assertEqual(chol_hamoed_3.action, Action.HAVDALAH.value)

        # Israel
        # 2023
        erev_pesach = Events(3, 1, 14, diaspora=False)  # 2023, 4, 5
        self.assertEqual(erev_pesach.action, Action.CANDLES.value)

        pesach_1 = Events(4, 1, 15, diaspora=False)  # 2023, 4, 6
        self.assertEqual(pesach_1.action, Action.HAVDALAH.value)

        chol_hamoed_1 = Events(5, 1, 16, diaspora=False)  # 2023, 4, 7
        self.assertEqual(chol_hamoed_1.action, Action.CANDLES.value)

        chol_hamoed_2 = Events(6, 1, 17, diaspora=False)  # 2023, 4, 8
        self.assertEqual(chol_hamoed_2.action, Action.HAVDALAH.value)

        # 2024
        chol_hamoed_3 = Events(5, 1, 18, diaspora=False)  # 2024, 4, 26
        self.assertEqual(chol_hamoed_3.action, Action.CANDLES.value)

        chol_hamoed_4 = Events(6, 1, 19, diaspora=False)  # 2024, 4, 27
        self.assertEqual(chol_hamoed_4.action, Action.HAVDALAH.value)

    def test_events_to_string(self) -> None:
        """Test `Events`-object to `str`."""
        # 2022, 4, 16 Shabbos, Pesach 1
        events = Events(6, 1, 15, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertEqual(events.yomtov, YOMTOV[1][15].title)
        self.assertEqual(events.action, YOMTOV[1][15].action)
        self.assertEqual(str(events), 'Shabbos, Pesach 1')

    def test_no_events_to_string(self) -> None:
        """Test no `Events`-object to `str`."""
        self.assertEqual(str(Events(4, 3, 14, diaspora=True)), '')

    def test_has_events(self) -> None:
        """Test events."""
        # 2022, 4, 16 Shabbos, Pesach 1
        events = Events(6, 1, 15, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertEqual(events.yomtov, YOMTOV[1][15].title)
        self.assertEqual(events.action, YOMTOV[1][15].action)
        self.assertTrue(events._has_events())

    def test_has_no_events(self) -> None:
        """Test no events."""
        self.assertFalse(Events(4, 3, 14, diaspora=True)._has_events())

    def test_is_erev_shabbos_and_not_is_shabbos(self) -> None:
        """Test Erev Shabbos."""
        events = Events(5, 3, 15, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[5].title)
        self.assertIsNone(events.yomtov)
        self.assertEqual(events.action, SHABBOS[5].action)
        self.assertTrue(events._is_erev_shabbos())
        self.assertFalse(events._is_shabbos())

    def test_is_not_erev_shabbos_and_is_shabbos(self) -> None:
        """Test it is Shabbos."""
        events = Events(6, 3, 16, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertIsNone(events.yomtov)
        self.assertEqual(events.action, SHABBOS[6].action)
        self.assertFalse(events._is_erev_shabbos())
        self.assertTrue(events._is_shabbos())

    def test_is_not_erev_shabbos_and_not_is_shabbos(self) -> None:
        """Test it is not (Erev) Shabbos."""
        events = Events(4, 3, 14, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertIsNone(events.yomtov)
        self.assertIsNone(events.action)
        self.assertFalse(events._is_erev_shabbos())
        self.assertFalse(events._is_shabbos())

    def test_is_erev_yomtov_and_not_is_yomtov(self) -> None:
        """Test Erev Yom Tov."""
        # 2024-09-02 Erev Rosh Hashana
        events = Events(3, 6, 29, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[6][29].title)
        self.assertEqual(events.action, YOMTOV[6][29].action)
        self.assertTrue(events._is_erev_yomtov())
        self.assertFalse(events._is_yomtov())

        # 2024-10-23 Hoshana Rabba (Sukkos 7)
        events = Events(3, 7, 21, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[7][21].title)
        self.assertEqual(events.action, YOMTOV[7][21].action)
        self.assertTrue(events._is_erev_yomtov())
        self.assertFalse(events._is_yomtov())

        # 2024-10-23 Hoshana Rabba (Sukkot 7)
        events = Events(3, 7, 21, diaspora=False)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[7][21].title)
        self.assertEqual(events.action, YOMTOV_ISRAEL[7][21].action)
        self.assertTrue(events._is_erev_yomtov())
        self.assertFalse(events._is_yomtov())

        # 2024-04-28 Chol HaMoed 4 (Pesach 6)
        events = Events(3, 1, 20, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[1][20].title)
        self.assertEqual(events.action, YOMTOV[1][20].action)
        self.assertTrue(events._is_erev_yomtov())
        self.assertFalse(events._is_yomtov())

        # Chol HaMoed 5 (Pesach 6)
        events = Events(3, 1, 20, diaspora=False)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[1][20].title)
        self.assertEqual(events.action, YOMTOV_ISRAEL[1][20].action)
        self.assertTrue(events._is_erev_yomtov())
        self.assertFalse(events._is_yomtov())

    def test_is_not_erev_yomtov_and_is_yomtov(self) -> None:
        """Test it is Yom Tov."""
        # 2024-09-03 Rosh Hashana 1
        events = Events(4, 7, 1, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[7][1].title)
        self.assertEqual(events.action, YOMTOV[7][1].action)
        self.assertFalse(events._is_erev_yomtov())
        self.assertTrue(events._is_yomtov())

    def test_is_not_erev_yomtov_and_not_is_yomtov(self) -> None:
        """Test it is not (Erev) Yom Tov."""
        # 2024-06-21
        events = Events(4, 3, 14, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertIsNone(events.yomtov)
        self.assertIsNone(events.action)
        self.assertFalse(events._is_erev_yomtov())
        self.assertFalse(events._is_yomtov())

        # 2024-04-25 Chol HaMoed 1 (Sukkos 3)
        events = Events(4, 7, 17, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[7][17].title)
        self.assertIsNone(events.action)
        self.assertFalse(events._is_erev_yomtov())
        self.assertFalse(events._is_yomtov())

    def test_is_erev(self) -> None:
        """Test it is Erev Shabbos and/or Erev Yom Tov."""
        # Diaspora
        # 2023, 9, 15  Erev Rosh Hashana
        events = Events(5, 6, 29, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[5].title)
        self.assertEqual(events.yomtov, YOMTOV[6][29].title)
        self.assertEqual(events.action, YOMTOV[6][29].action)
        self.assertTrue(events._is_erev())

        # 2024, 4, 22 Erev Pesach
        events = Events(1, 1, 14, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[1][14].title)
        self.assertEqual(events.action, YOMTOV[1][14].action)
        self.assertTrue(events._is_erev())

        # 2024, 4, 26  Chol HaMoed 2 (Pesach 4)
        events = Events(5, 1, 18, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[5].title)
        self.assertEqual(events.yomtov, YOMTOV[1][18].title)
        self.assertEqual(events.action, Action.CANDLES.value)
        self.assertTrue(events._is_erev())

        # Israel
        # 2023, 9, 22
        events = Events(5, 7, 7, diaspora=False)
        self.assertEqual(events.shabbos, SHABBOS[5].title)
        self.assertIsNone(events.yomtov)
        self.assertEqual(events.action, SHABBOS[5].action)
        self.assertTrue(events._is_erev())

        # 2024, 4, 26 Chol HaMoed 3 (Pesach 4)
        events = Events(5, 1, 18, diaspora=False)
        self.assertEqual(events.shabbos, SHABBOS[5].title)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[1][18].title)
        self.assertEqual(events.action, Action.CANDLES.value)
        self.assertTrue(events._is_erev())

        # 2024, 10, 2 Erev Rosh Hashana
        events = Events(3, 6, 29, diaspora=False)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[6][29].title)
        self.assertEqual(events.action, YOMTOV_ISRAEL[6][29].action)
        self.assertTrue(events._is_erev())

    def test_is_not_erev(self) -> None:
        """Test it is not Erev Shabbos and/or Erev Yom Tov."""
        # Diaspora
        # 2023, 9, 16 Rosh Hashana 1
        events = Events(6, 7, 1, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertEqual(events.yomtov, YOMTOV[7][1].title)
        self.assertEqual(events.action, YOMTOV[7][1].action)
        self.assertFalse(events._is_erev())

        # 2023, 9, 17 Rosh Hashana 2
        events = Events(0, 7, 2, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[7][2].title)
        self.assertEqual(events.action, YOMTOV[7][2].action)
        self.assertFalse(events._is_erev())

        # 2024, 4, 25 Chol HaMoed 1 (Pesach 3)
        events = Events(4, 1, 17, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[1][17].title)
        self.assertIsNone(events.action)
        self.assertFalse(events._is_erev())

        # 2024, 4, 27 Chol HaMoed 3 (Pesach 5)
        events = Events(6, 1, 19, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertEqual(events.yomtov, YOMTOV[1][19].title)
        self.assertEqual(events.action, Action.HAVDALAH.value)
        self.assertFalse(events._is_erev())

        # Israel
        # 2024, 4, 23 Pesach 1
        events = Events(2, 1, 15, diaspora=False)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[1][15].title)
        self.assertEqual(events.action, YOMTOV_ISRAEL[1][15].action)
        self.assertFalse(events._is_erev())

        # 2024, 4, 24 Chol HaMoed 1 (Pesach 2)
        events = Events(3, 1, 16, diaspora=False)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[1][16].title)
        self.assertIsNone(events.action)
        self.assertFalse(events._is_erev())

        # 2024, 4, 27 Chol HaMoed 4 (Pesach 5)
        events = Events(6, 1, 19, diaspora=False)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[1][19].title)
        self.assertEqual(events.action, Action.HAVDALAH.value)
        self.assertFalse(events._is_erev())

        # 2024, 10, 3 Rosh Hashana 1
        events = Events(4, 7, 1, diaspora=False)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[7][1].title)
        self.assertEqual(events.action, YOMTOV_ISRAEL[7][1].action)
        self.assertFalse(events._is_erev())

        # 2024, 10, 4 Rosh Hashana 2
        events = Events(5, 7, 2, diaspora=False)
        self.assertEqual(events.shabbos, SHABBOS[5].title)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[7][2].title)
        self.assertEqual(events.action, Action.CANDLES.value)
        self.assertFalse(events._is_erev())

    def test_is_issur_melacha(self) -> None:
        """Test it is Issur melacha."""
        # Diaspora
        # 2024-06-22
        events = Events(6, 3, 16, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertIsNone(events.yomtov)
        self.assertEqual(events.action, SHABBOS[6].action)
        self.assertTrue(events._is_issur_melacha())

        # 2023, 4, 6 Pesach 1
        events = Events(4, 1, 15, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[1][15].title)
        self.assertEqual(events.action, YOMTOV[1][15].action)
        self.assertTrue(events._is_issur_melacha())

        # 2023, 4, 7 Pesach 2
        events = Events(5, 1, 16, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[5].title)
        self.assertEqual(events.yomtov, YOMTOV[1][16].title)
        self.assertEqual(events.action, Action.CANDLES.value)
        self.assertTrue(events._is_issur_melacha())

        # 2023, 4, 8 Chol HaMoed 1 (Pesach 3)
        events = Events(6, 1, 17, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertEqual(events.yomtov, YOMTOV[1][17].title)
        self.assertEqual(events.action, Action.HAVDALAH.value)
        self.assertTrue(events._is_issur_melacha())

        # Israel
        # 2023, 4, 6 Pesach 1
        events = Events(4, 1, 15, diaspora=False)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[1][15].title)
        self.assertEqual(events.action, YOMTOV_ISRAEL[1][15].action)
        self.assertTrue(events._is_issur_melacha())

        # 2023, 4, 8 Chol HaMoed 1 (Pesach 3)
        events = Events(6, 1, 17, diaspora=False)
        self.assertEqual(events.shabbos, SHABBOS[6].title)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[1][17].title)
        self.assertEqual(events.action, Action.HAVDALAH.value)
        self.assertTrue(events._is_issur_melacha())

    def test_is_not_issur_melacha(self) -> None:
        """Test it is not Issur melacha."""
        # Diaspora
        events = Events(5, 3, 15, diaspora=True)
        self.assertEqual(events.shabbos, SHABBOS[5].title)
        self.assertIsNone(events.yomtov)
        self.assertEqual(events.action, SHABBOS[5].action)
        self.assertFalse(events._is_issur_melacha())

        # 2023, 4, 5 Erev Pesach
        events = Events(3, 1, 14, diaspora=True)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV[1][14].title)
        self.assertEqual(events.action, YOMTOV[1][14].action)
        self.assertFalse(events._is_issur_melacha())

        # Israel
        # 2023, 4, 5  YOMTOV_ISRAEL[1][14].title)
        events = Events(3, 1, 14, diaspora=False)
        self.assertIsNone(events.shabbos)
        self.assertEqual(events.yomtov, YOMTOV_ISRAEL[1][14].title)
        self.assertEqual(events.action, YOMTOV_ISRAEL[1][14].action)
        self.assertFalse(events._is_issur_melacha())

        # 2023, 4, 7 Chol HaMoed 1 (Pesach 2)
        events = Events(5, 1, 16, diaspora=False)
        self.assertTrue(events.shabbos, SHABBOS[5].title)
        self.assertTrue(events.yomtov, YOMTOV_ISRAEL[1][16].title)
        self.assertTrue(events.action, YOMTOV_ISRAEL[1][16].action)
        self.assertFalse(events._is_issur_melacha())
