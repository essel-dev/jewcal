"""Derive the time for sun positions (USNO algorithm).

Based on the source code from Ulrich and David Greve (2005)
https://www.david-greve.de/luach-code/jewish-python.html
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import Enum, unique
from math import acos, atan, cos, degrees, fabs, floor, pi, sin, sqrt, tan
from typing import Final

ZENITH_DEG_HORIZON: Final[float] = 90
ZENITH_MIN_HORIZON: Final[float] = 50
HOUR_ANGLE: Final[float] = 15
RAD_DEG: Final[float] = 180 / pi
ROTATION_DEG = 360  # Sun is one revolution per day, that is 360° every 24 hours


@unique
class SunEvent(Enum):
    """Enum for sunrise and sunset."""

    RISE = 'sunrise'
    SET = 'sunset'


class SunEventError(Exception):
    """Sun exceptions."""

    def __init__(
        self,
        message: str = f'Use {SunEvent.RISE.value} or {SunEvent.SET.value}.',
    ) -> None:
        """Initialize.

        Args:
            message: The error message.
        """
        self.message = message
        super().__init__(self.message)


@dataclass
class Sun:
    """Sun positions for a geographic location on a certain date.

    Get the times in UTC for:
        - sunrise
        - sunset
        - the sun at a certain degrees below horizon
    """

    date: date
    """The date to use for the sun events."""

    latitude: float
    """The latitude in decimal degrees.

    Example:
        - Decimal degrees (DD): 41.40338
    """

    longitude: float
    """The longitude in decimal degrees.

    Example:
        - Decimal degrees (DD): 2.17403
    """

    elevation: float = 0
    """The sea level in meters."""

    sunrise: datetime = field(init=False)
    """The time for sunrise."""

    sunset: datetime = field(init=False)
    """The time for sunset."""

    def __post_init__(self) -> None:
        """Set sunrise and sunset times."""
        self.sunrise, self.sunset = self._sunrise_equation()

    def deg_below_horizon(
        self,
        deg_below_horizon: float,
        sun_event: SunEvent,
    ) -> datetime:
        """Get the time for the sun at a certain degrees below horizon.

        Args:
            deg_below_horizon: The degrees below horizon.
            sun_event: The sun event (sunrise or sunset).

        Returns:
            The time.
        """
        zenith_adjusted = deg_below_horizon + ZENITH_DEG_HORIZON
        zenith_deg = floor(zenith_adjusted)
        zenith_min = floor((zenith_adjusted - zenith_deg) * 60)
        sunset_below = self._sunrise_equation(zenith_deg, zenith_min)[1]

        sunset_minutes = self.sunset.hour * 60 + self.sunset.minute
        sunset_below_minutes = sunset_below.hour * 60 + sunset_below.minute

        delta_minutes = sunset_below_minutes - sunset_minutes

        match sun_event:
            case SunEvent.RISE:
                return self.sunrise - timedelta(minutes=delta_minutes)
            case SunEvent.SET:
                return self.sunset + timedelta(minutes=delta_minutes)

    def _sunrise_equation(  # pylint: disable=too-many-locals
        self,
        zenith_deg: float = ZENITH_DEG_HORIZON,
        zenith_min: float = ZENITH_MIN_HORIZON,
    ) -> tuple[datetime, datetime]:
        """Get the times for sunrise and sunset.

        Sunrise and sunset occur when the zenith angle is at 90° 50'.

        To get the times at a certain point below horizon, adjust:
            - ``zenith_deg``.
            - ``zenith_min``.

        Args:
            zenith_deg: The zenith position in degrees.
            zenith_min: The zenith position in minutes.

        Returns:
            The times for sunrise and sunset.
        """
        # local hour angle
        local_hour_angle = self._local_hour_angle()

        # local apparent time
        sunrise_local_apparent_time = self._local_apparent_time(
            local_hour_angle,
            SunEvent.RISE,
        )
        sunset_local_apparent_time = self._local_apparent_time(
            local_hour_angle,
            SunEvent.SET,
        )

        # local mean time
        sunrise_local_mean_time = self._local_mean_time(sunrise_local_apparent_time)
        sunset_local_mean_time = self._local_mean_time(sunset_local_apparent_time)

        # mean anomaly
        sunrise_mean_anomaly = self._mean_anomaly(sunrise_local_apparent_time)
        sunset_mean_anomaly = self._mean_anomaly(sunset_local_apparent_time)

        # true longitude
        sunrise_true_longitude = self._true_longitude(sunrise_mean_anomaly)
        sunset_true_longitude = self._true_longitude(sunset_mean_anomaly)

        # declination
        sun_declination = self._declination(
            sunrise_true_longitude,
            zenith_deg,
            zenith_min,
        )

        # solar hour angle
        sunrise_solar_hour_angle = self._solar_hour_angle(
            sun_declination,
            SunEvent.RISE,
        )
        sunset_solar_hour_angle = self._solar_hour_angle(
            sun_declination,
            SunEvent.SET,
        )

        # right ascension hour angle
        sunrise_right_ascension_hour_angle = self._right_ascension_hour_angle(
            sunrise_true_longitude,
        )
        sunset_right_ascension_hour_angle = self._right_ascension_hour_angle(
            sunset_true_longitude,
        )

        # datetime
        sunrise_utc = self.__utc_time(
            sunrise_solar_hour_angle,
            sunrise_right_ascension_hour_angle,
            sunrise_local_mean_time,
            local_hour_angle,
        )
        sunset_utc = self.__utc_time(
            sunset_solar_hour_angle,
            sunset_right_ascension_hour_angle,
            sunset_local_mean_time,
            local_hour_angle,
        )

        return sunrise_utc, sunset_utc

    def _local_hour_angle(self) -> float:
        """Get the local hour angle.

        Returns:
            The local hour angle.
        """
        longitude = float(self.longitude * 100)
        longitude_deg, longitude_min = self.__dd_to_ddm(longitude)
        longitude = self.__ddm_to_dd(longitude_deg, longitude_min)

        if self.__is_east_of_meridian():
            longitude *= -1

        return longitude / HOUR_ANGLE

    def _local_apparent_time(
        self,
        local_hour_angle: float,
        sun_event: SunEvent,
    ) -> float:
        """Get the local apparent time for sunrise or sunset.

        Args:
            local_hour_angle: The local hour angle.
            sun_event: The sun event (sunrise or sunset).

        Returns:
            The time.
        """
        day = self.date.timetuple().tm_yday + 1

        match sun_event:
            case SunEvent.RISE:
                return day + (6 + local_hour_angle) / 24
            case SunEvent.SET:
                return day + (18 + local_hour_angle) / 24

    def _local_mean_time(self, local_apparent_time: float) -> float:
        """Get the local mean time.

        Args:
            local_apparent_time: The local apparent time.

        Returns:
            The local mean time.
        """
        return -0.06571 * local_apparent_time - 6.620

    def _mean_anomaly(self, local_apparent_time: float) -> float:
        """Get the mean anomaly.

        Args:
            local_apparent_time: The local apparent time.

        Returns:
            The mean anomaly.
        """
        return ROTATION_DEG / 365.25 * local_apparent_time - 3.251

    def _true_longitude(self, mean_anomaly: float) -> float:
        """Get the true longitude.

        Args:
            mean_anomaly: The mean anomaly.

        Returns:
            The true longitude.
        """
        return (
            mean_anomaly
            + 1.916 * sin(0.01745 * mean_anomaly)
            + 0.02 * sin(2 * 0.01745 * mean_anomaly)
            + 282.565
        )

    def _declination(  # pylint: disable=too-many-locals
        self,
        sunrise_true_longitude: float,
        zenith_deg: float,
        zenith_min: float,
    ) -> float:
        """Get the declination.

        Args:
            sunrise_true_longitude: The true longitude for sunrise.
            zenith_deg: The zenith position in degrees.
            zenith_min: The zenith position in minutes.

        Returns:
            The declination.

        Raises:
            SunEventError: If there is no sunrise/sunset at this location.
        """
        if zenith_deg == ZENITH_DEG_HORIZON:
            earth_radius_meters = 6356.9 * 1000
            elevation_adjusted = degrees(
                acos(earth_radius_meters / (earth_radius_meters + self.elevation)),
            )

            zenith_adjusted = (
                self.__ddm_to_dd(zenith_deg, zenith_min) + elevation_adjusted
            )
            zenith_deg = floor(zenith_adjusted)
            zenith_min = (zenith_adjusted - floor(zenith_adjusted)) * 60
        zenith_cos = cos(0.01745 * self.__ddm_to_dd(zenith_deg, zenith_min))

        declination_sin = 0.39782 * sin(0.01745 * sunrise_true_longitude)
        declination_cos = sqrt(1 - declination_sin * declination_sin)

        latitude_deg, latitude_min = self.__dd_to_ddm(float(self.latitude * 100))
        latitude = self.__ddm_to_dd(latitude_deg, latitude_min)
        if not self.__is_above_equator():
            latitude *= -1
        latitude_cos = cos(0.01745 * latitude)
        latitude_sin = sin(0.01745 * latitude)

        declination = (zenith_cos - declination_sin * latitude_sin) / (
            declination_cos * latitude_cos
        )
        if abs(declination) <= 1:
            return RAD_DEG * acos(declination)
        error = 'No sunrise/sunset at this location'
        raise SunEventError(error)

    def _solar_hour_angle(
        self,
        sunrise_declination: float,
        sun_event: SunEvent,
    ) -> float:
        """Get the solar hour angle.

        Args:
            sunrise_declination: The declination at sunrise.
            sun_event: The sun event (sunrise or sunset).

        Returns:
            The solar hour angle.
        """
        match sun_event:
            case SunEvent.RISE:
                return ROTATION_DEG - sunrise_declination / HOUR_ANGLE
            case SunEvent.SET:
                return sunrise_declination / HOUR_ANGLE

    def _right_ascension_hour_angle(self, true_longitude: float) -> float:
        """Get the right ascension hour angle.

        Args:
            true_longitude: The true longitude.

        Returns:
            The right ascension hour angle.
        """
        # right ascension
        right_ascension = RAD_DEG * atan(0.91746 * tan(0.01745 * true_longitude))

        # right ascension value must be in same quadrant as true_longitude
        if abs(right_ascension + ROTATION_DEG - true_longitude) > ZENITH_DEG_HORIZON:
            right_ascension += 180.0
        if right_ascension > ROTATION_DEG:
            right_ascension -= ROTATION_DEG

        # right ascension to hour angle
        return right_ascension / HOUR_ANGLE

    def __utc_time(
        self,
        solar_hour_angle: float,
        right_ascension_hour_angle: float,
        local_mean_time: float,
        local_hour_angle: float,
    ) -> datetime:
        """Get the time in UTC.

        Args:
            solar_hour_angle: The solar hour angle.
            right_ascension_hour_angle: The right ascension hour angle.
            local_mean_time:  The local mean time.
            local_hour_angle: The local hour angle.

        Returns:
            The time in UTC.
        """
        utc = (
            solar_hour_angle
            + right_ascension_hour_angle
            + local_mean_time
            + local_hour_angle
        )

        if utc < 0:
            utc += 24

        time_of_day = utc % 24

        hours, rest = divmod(time_of_day * 3600, 3600)
        minutes, rest = divmod(rest, 60)
        seconds, microseconds = divmod(rest * 10**6, 10**6)

        return datetime(
            self.date.year,
            self.date.month,
            self.date.day,
            int(hours),
            int(minutes),
            int(seconds),
            int(microseconds),
            tzinfo=timezone.utc,
        )

    def __is_above_equator(self) -> bool:
        """Is the latitude above the equator.

        Positive latitudes are North, negative latitudes are South.

        Returns:
            True if above the equator, False otherwise.
        """
        return bool(self.latitude >= 0)

    def __is_east_of_meridian(self) -> bool:
        """Is the longitude east of the meridian.

        Positive longitudes are East, negative longitudes are West.

        Returns:
            True if east of the meridian, False otherwise.
        """
        return bool(self.longitude >= 0)

    def __ddm_to_dd(self, deg: float, dec_min: float) -> float:
        """Convert degrees and decimal minutes (DDM) to decimal degrees (DD).

        Example:
            - Decimal degrees (DD): 41.40338, 2.17403
            - Degrees, minutes, and seconds (DMS): 41°24'12.2"N 2°10'26.5"E
            - Degrees and decimal minutes (DDM): 41 24.2028, 2 10.4418

        Args:
            deg: The degrees.
            dec_min: The decimal minutes.

        Returns:
            The decimal degrees.
        """
        return deg + dec_min / 60

    def __dd_to_ddm(self, dec_deg: float) -> tuple[float, float]:
        """Convert decimal degrees (DD) to degrees and decimal minutes (DDM).

        Example:
            - Decimal degrees (DD): 41.40338, 2.17403
            - Degrees, minutes, and seconds (DMS): 41°24'12.2"N 2°10'26.5"E
            - Degrees and decimal minutes (DDM): 41 24.2028, 2 10.4418

        Args:
            dec_deg: The decimal degrees.

        Returns:
            The degrees and decimal minutes.
        """
        deg = float(floor(fabs(dec_deg / 100)))
        dec_min = abs(dec_deg) % 100

        return deg, dec_min
