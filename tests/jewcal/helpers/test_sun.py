"""Unittests for jewcal.helpers.sun."""

from datetime import date, datetime, timezone
from unittest import TestCase

from src.jewcal.helpers.sun import Sun, SunEvent


class SunTestCase(TestCase):
    """Unittests for sun."""

    def test_init(self) -> None:
        """Test init."""
        lat, lon = 51.22047, 4.40026

        expected_sunrise = datetime(2024, 5, 31, 3, 29, 55, 470753, tzinfo=timezone.utc)
        expected_sunset = datetime(2024, 5, 31, 19, 47, 51, 641803, tzinfo=timezone.utc)

        sun = Sun(date(2024, 5, 31), lat, lon)

        self.assertEqual(expected_sunrise, sun.sunrise)
        self.assertEqual(expected_sunset, sun.sunset)

    def test_deg_below_horizon(self) -> None:
        """Test the sun at degrees below the horizon."""
        expected_tzeis_hakochavim = datetime(
            2024,
            6,
            1,
            20,
            59,
            55,
            50901,
            tzinfo=timezone.utc,
        )

        lat, lon = 51.22047, 4.40026
        sun = Sun(date(2024, 6, 1), lat, lon)

        self.assertEqual(
            expected_tzeis_hakochavim,
            sun.deg_below_horizon(8.5, SunEvent.SET),
        )
