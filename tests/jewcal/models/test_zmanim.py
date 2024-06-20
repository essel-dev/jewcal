"""Unittests for jewcal.models.zmanim."""

from datetime import date, datetime, timezone
from unittest import TestCase
from unittest.mock import Mock, patch

from src.jewcal.models.zmanim import Location, Zmanim


class ZmanimTestCase(TestCase):
    """Unittests for Zmanim."""

    def test_to_dict(self) -> None:
        """Test to_dict."""
        expected_keys = [
            'sunrise',
            'sunset',
            'plag_hamincha',
            'hadlokas_haneiros',
            'tzeis_hakochavim',
            'tzeis_minutes',
        ]

        lat, lon = 51.22047, 4.40026
        location = Location(latitude=lat, longitude=lon)
        zmanim = Zmanim(date(2024, 5, 31), location)

        self.assertEqual(sorted(zmanim.to_dict().keys()), sorted(expected_keys))

    def test_set_zmanim(self) -> None:
        """Test Zmanim.

        Raises:
            TypeError: If Zmanim is `None`
        """
        # Antwerpen
        lat, lon = 51.22047, 4.40026
        location = Location(latitude=lat, longitude=lon)

        # erev shabbos
        expected_plag = datetime(2024, 5, 31, 18, 5, 59, 540654, tzinfo=timezone.utc)
        expected_neiros = datetime(2024, 5, 31, 19, 29, 51, 641803, tzinfo=timezone.utc)
        erev_shabbos = Zmanim(date(2024, 5, 31), location, set_hadlokas_haneiros=True)
        self.assertEqual(expected_plag, erev_shabbos.plag_hamincha)
        self.assertEqual(expected_neiros, erev_shabbos.hadlokas_haneiros)

        # motse shabbos
        expected_kochavim = datetime(2024, 6, 1, 20, 59, 55, 50901, tzinfo=timezone.utc)
        expected_minutes = datetime(2024, 6, 1, 21, 0, 55, 50901, tzinfo=timezone.utc)
        shabbos = Zmanim(date(2024, 6, 1), location)
        self.assertEqual(expected_kochavim, shabbos.tzeis_hakochavim)
        self.assertEqual(expected_minutes, shabbos.tzeis_minutes)

        # Jerushalayim
        lat, lon = 31.76904, 35.21633

        location = Location(
            latitude=lat,
            longitude=lon,
            hadlokas_haneiros_minutes=40,
        )

        # erev shabbos
        expected_plag = datetime(2024, 6, 21, 15, 19, 6, 523393, tzinfo=timezone.utc)
        expected_neiros = datetime(2024, 6, 21, 16, 8, 16, 510134, tzinfo=timezone.utc)
        erev_shabbos = Zmanim(date(2024, 6, 21), location, set_hadlokas_haneiros=True)
        self.assertEqual(expected_plag, erev_shabbos.plag_hamincha)
        self.assertEqual(expected_neiros, erev_shabbos.hadlokas_haneiros)

        # motse shabbos
        expected_kochavim = datetime(
            2024,
            6,
            22,
            17,
            31,
            26,
            984992,
            tzinfo=timezone.utc,
        )
        expected_minutes = datetime(2024, 6, 22, 18, 0, 26, 984992, tzinfo=timezone.utc)
        shabbos = Zmanim(date(2024, 6, 22), location)
        self.assertEqual(expected_kochavim, shabbos.tzeis_hakochavim)
        self.assertEqual(expected_minutes, shabbos.tzeis_minutes)

    @patch('src.jewcal.models.zmanim.datetime_now', autospec=True)
    @patch('src.jewcal.models.zmanim.date_today', autospec=True)
    def test_is_now_after_nightfall_true(
        self,
        mock_today: Mock,
        mock_now: Mock,
    ) -> None:
        """Test now is after nightfall."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        mock_today.return_value = date(2024, 5, 31)
        mock_now.return_value = datetime(2024, 5, 31, 23, 30, 0, tzinfo=timezone.utc)
        zmanim = Zmanim(date(2024, 5, 31), location)
        self.assertTrue(
            zmanim.is_now_after_nightfall(
                use_tzeis_hakochavim=location.use_tzeis_hakochavim,
            ),
        )

    @patch('src.jewcal.models.zmanim.datetime_now', autospec=True)
    @patch('src.jewcal.models.zmanim.date_today', autospec=True)
    def test_is_now_after_nightfall_false(
        self,
        mock_today: Mock,
        mock_now: Mock,
    ) -> None:
        """Test now is not after nightfall."""
        lat, lon = 51.22047, 4.40026  # Antwerpen
        location = Location(latitude=lat, longitude=lon)

        mock_today.return_value = date(2024, 5, 31)
        mock_now.return_value = datetime(2024, 5, 31, 13, 30, 0, tzinfo=timezone.utc)
        zmanim = Zmanim(date(2024, 5, 31), location)
        self.assertFalse(
            zmanim.is_now_after_nightfall(
                use_tzeis_hakochavim=location.use_tzeis_hakochavim,
            ),
        )
