"""Unittests for jewcal.models.events."""

from unittest import TestCase

from jewcal.constants import SHABBOS, YOMTOV, YOMTOV_ISRAEL

from src.jewcal.models.events import Events

# ruff: noqa: SLF001
# pylint: disable=W0212


class EventsTestCase(TestCase):
    """Unittests for Events."""

    def setUp(self) -> None:
        """Initialize."""
        self.events = Events()

    def tearDown(self) -> None:
        """Clean up after tests."""
        self.events = Events()

    def test_events_to_string(self) -> None:
        """Test `Events`-object to `str`."""
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = YOMTOV[1][15].title
        self.events.action = YOMTOV[1][15].action
        self.assertEqual(str(self.events), 'Shabbos, Pesach 1')

    def test_no_events_to_string(self) -> None:
        """Test no `Events`-object to `str`."""
        self.assertEqual(str(Events()), '')

    def test_has_events(self) -> None:
        """Test events."""
        self.events.shabbos = SHABBOS[6].title  # Shabbos
        self.events.yomtov = YOMTOV[1][15].title  # Pesach 1
        self.events.action = YOMTOV[1][15].action
        self.assertTrue(self.events._has_events())

    def test_has_no_events(self) -> None:
        """Test no events."""
        self.assertFalse(Events()._has_events())

    def test_is_erev_shabbos_and_not_is_shabbos(self) -> None:
        """Test Erev Shabbos."""
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = None
        self.events.action = SHABBOS[5].action
        self.assertTrue(self.events._is_erev_shabbos())
        self.assertFalse(self.events._is_shabbos())

    def test_is_not_erev_shabbos_and_is_shabbos(self) -> None:
        """Test it is Shabbos."""
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = None
        self.events.action = SHABBOS[6].action
        self.assertFalse(self.events._is_erev_shabbos())
        self.assertTrue(self.events._is_shabbos())

    def test_is_not_erev_shabbos_and_not_is_shabbos(self) -> None:
        """Test it is not (Erev) Shabbos."""
        self.events.shabbos = None
        self.events.yomtov = None
        self.events.action = None
        self.assertFalse(self.events._is_erev_shabbos())
        self.assertFalse(self.events._is_shabbos())

    def test_is_erev_yomtov_and_not_is_yomtov(self) -> None:
        """Test Erev Yom Tov."""
        self.events.shabbos = None
        self.events.yomtov = YOMTOV[6][29].title  # Erev Rosh Hashana
        self.events.action = YOMTOV[6][29].action
        self.assertTrue(self.events._is_erev_yomtov())
        self.assertFalse(self.events._is_yomtov())

        self.events.shabbos = None
        self.events.yomtov = YOMTOV[7][21].title  # Hoshana Rabba (Sukkos 7)
        self.events.action = YOMTOV[7][21].action
        self.assertTrue(self.events._is_erev_yomtov())
        self.assertFalse(self.events._is_yomtov())

        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[7][21].title  # Hoshana Rabba (Sukkot 7)
        self.events.action = YOMTOV_ISRAEL[7][21].action
        self.assertTrue(self.events._is_erev_yomtov())
        self.assertFalse(self.events._is_yomtov())

        self.events.shabbos = None
        self.events.yomtov = YOMTOV[1][20].title  # Chol HaMoed 4 (Pesach 6)
        self.events.action = YOMTOV[1][20].action
        self.assertTrue(self.events._is_erev_yomtov())
        self.assertFalse(self.events._is_yomtov())

        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[1][20].title  # Chol HaMoed 5 (Pesach 6)
        self.events.action = YOMTOV_ISRAEL[1][20].action
        self.assertTrue(self.events._is_erev_yomtov())
        self.assertFalse(self.events._is_yomtov())

    def test_is_not_erev_yomtov_and_is_yomtov(self) -> None:
        """Test it is Yom Tov."""
        self.events.shabbos = None
        self.events.yomtov = YOMTOV[7][1].title  # Rosh Hashana 1
        self.events.action = YOMTOV[7][1].action
        self.assertFalse(self.events._is_erev_yomtov())
        self.assertTrue(self.events._is_yomtov())

    def test_is_not_erev_yomtov_and_not_is_yomtov(self) -> None:
        """Test it is not (Erev) Yom Tov."""
        self.events.shabbos = None
        self.events.yomtov = None
        self.events.action = None
        self.assertFalse(self.events._is_erev_yomtov())
        self.assertFalse(self.events._is_yomtov())

        self.events.shabbos = None
        self.events.yomtov = YOMTOV[7][17].title  # Chol HaMoed 1 (Sukkos 3)
        self.events.action = None
        self.assertFalse(self.events._is_erev_yomtov())
        self.assertFalse(self.events._is_yomtov())

    def test_is_erev(self) -> None:
        """Test it is Erev Shabbos and/or Erev Yom Tov."""
        # Diaspora
        # 2023, 9, 15
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = YOMTOV[6][29].title  # Erev Rosh Hashana
        self.events.action = YOMTOV[6][29].action
        self.assertTrue(self.events._is_erev())

        # 2024, 4, 22
        self.events.shabbos = None
        self.events.yomtov = YOMTOV[1][14].title  # Erev Pesach
        self.events.action = YOMTOV[1][14].action
        self.assertTrue(self.events._is_erev())

        # 2024, 4, 26
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = YOMTOV[1][18].title  # Chol HaMoed 2 (Pesach 4)
        self.events.action = 'Candles'  # adjusted through JewCal initialization
        self.assertTrue(self.events._is_erev())

        # Israel
        # 2023, 9, 22
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = None
        self.events.action = SHABBOS[5].action
        self.assertTrue(self.events._is_erev())

        # 2024, 4, 22
        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[1][14].title  # Erev Pesach
        self.events.action = YOMTOV_ISRAEL[1][14].action
        self.assertTrue(self.events._is_erev())

        # 2024, 4, 26
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = YOMTOV_ISRAEL[1][18].title  # Chol HaMoed 3 (Pesach 4)
        self.events.action = 'Candles'  # adjusted through JewCal initialization
        self.assertTrue(self.events._is_erev())

        # 2024, 10, 2
        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[6][29].title  # Erev Rosh Hashana
        self.events.action = YOMTOV_ISRAEL[6][29].action
        self.assertTrue(self.events._is_erev())

    def test_is_not_erev(self) -> None:
        """Test it is not Erev Shabbos and/or Erev Yom Tov."""
        # Diaspora
        # 2023, 9, 16
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = YOMTOV[7][1].title  # Rosh Hashana 1
        self.events.action = YOMTOV[7][1].action
        self.assertFalse(self.events._is_erev())

        # 2023, 9, 17
        self.events.shabbos = None
        self.events.yomtov = YOMTOV[7][2].title  # Rosh Hashana 2
        self.events.action = YOMTOV[7][2].action
        self.assertFalse(self.events._is_erev())

        # 2024, 4, 25
        self.events.shabbos = None
        self.events.yomtov = YOMTOV[1][17].title  # Chol HaMoed 1 (Pesach 3)'
        self.events.action = None
        self.assertFalse(self.events._is_erev())

        # 2024, 4, 27
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = YOMTOV[1][19].title  # Chol HaMoed 3 (Pesach 5)'
        self.events.action = YOMTOV[1][19].action
        self.assertFalse(self.events._is_erev())

        # 2024, 10, 3
        self.events.shabbos = None
        self.events.yomtov = YOMTOV[7][1].title  # Rosh Hashana 1
        self.events.action = YOMTOV[7][1].action
        self.assertFalse(self.events._is_erev())

        # 2024, 10, 4
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = YOMTOV[7][2].title  # Rosh Hashana 2
        self.events.action = YOMTOV[7][2].action
        self.assertFalse(self.events._is_erev())

        # 2024, 10, 5
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = None
        self.events.action = SHABBOS[6].action
        self.assertFalse(self.events._is_erev())

        # Israel
        # 2024, 4, 23
        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[1][15].title
        self.events.action = YOMTOV_ISRAEL[1][15].action
        self.assertFalse(self.events._is_erev())

        # 2024, 4, 24
        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[1][16].title  # Chol HaMoed 1 (Pesach 2)
        self.events.action = None
        self.assertFalse(self.events._is_erev())

        # 2024, 4, 27
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = YOMTOV_ISRAEL[1][19].title  # Chol HaMoed 4 (Pesach 5)
        self.events.action = YOMTOV_ISRAEL[1][19].action
        self.assertFalse(self.events._is_erev())

        # 2024, 10, 3
        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[7][1].title  # Rosh Hashana 1
        self.events.action = YOMTOV_ISRAEL[7][1].action
        self.assertFalse(self.events._is_erev())

        # 2024, 10, 4
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = YOMTOV_ISRAEL[7][2].title  # Rosh Hashana 2
        self.events.action = YOMTOV_ISRAEL[7][2].action
        self.assertFalse(self.events._is_erev())

    def test_is_issur_melacha(self) -> None:
        """Test it is Issur melacha."""
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = None
        self.events.action = SHABBOS[6].action
        self.assertTrue(self.events._is_issur_melacha())

        # Diaspora
        # 2023, 4, 6
        self.events.shabbos = None
        self.events.yomtov = YOMTOV[1][15].title
        self.events.action = YOMTOV[1][15].action
        self.assertTrue(self.events._is_issur_melacha())

        # 2023, 4, 7
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = YOMTOV[1][16].title  # Pesach 2
        self.events.action = YOMTOV[1][16].action
        self.assertTrue(self.events._is_issur_melacha())

        # 2023, 4, 8
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = YOMTOV[1][17].title  # Chol HaMoed 1 (Pesach 3)
        self.events.action = 'Hadalah'  # adjusted through JewCal initialization
        self.assertTrue(self.events._is_issur_melacha())

        # Israel
        # 2023, 4, 6
        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[1][15].title  # Pesach 1
        self.events.action = YOMTOV_ISRAEL[1][15].action
        self.assertTrue(self.events._is_issur_melacha())

        # 2023, 4, 8
        self.events.shabbos = SHABBOS[6].title
        self.events.yomtov = YOMTOV_ISRAEL[1][17].title  # Chol HaMoed 1 (Pesach 3)
        self.events.action = 'Hadalah'  # adjusted through JewCal initialization
        self.assertTrue(self.events._is_issur_melacha())

    def test_is_not_issur_melacha(self) -> None:
        """Test it is not Issur melacha."""
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = None
        self.events.action = SHABBOS[5].action
        self.assertFalse(self.events._is_issur_melacha())

        # Diaspora
        # 2023, 4, 5
        self.events.shabbos = None
        self.events.yomtov = YOMTOV[1][14].title  # Erev Pesach
        self.events.action = YOMTOV[1][14].action
        self.assertFalse(self.events._is_issur_melacha())

        # Israel
        # 2023, 4, 5
        self.events.shabbos = None
        self.events.yomtov = YOMTOV_ISRAEL[1][14].title  # Erev Pesach
        self.events.action = YOMTOV_ISRAEL[1][14].action
        self.assertFalse(self.events._is_issur_melacha())

        # 2023, 4, 7
        self.events.shabbos = SHABBOS[5].title
        self.events.yomtov = YOMTOV_ISRAEL[1][16].title  # Chol HaMoed 1 (Pesach 2)
        self.events.action = YOMTOV_ISRAEL[1][16].action
        self.assertFalse(self.events._is_issur_melacha())
