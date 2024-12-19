"""Get sunrise, sunset using `Astral` library."""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum, unique

from astral import LocationInfo, Observer, SunDirection
from astral.sun import sun, time_at_elevation


@unique
class SunEvent(Enum):
    """Enum for sunrise and sunset."""

    RISE = 'sunrise'
    SET = 'sunset'


@dataclass
class Sun:
    """Sun positions for a geographic location on a certain date.

    Get the times in UTC for:
        - sunrise
        - sunset
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
    """The time for sunrise in UTC."""

    sunset: datetime = field(init=False)
    """The time for sunset in UTC."""

    observer: Observer = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Set sunrise and sunset times."""
        location = LocationInfo('', '', '', self.latitude, self.longitude)
        self.observer = location.observer

        s = sun(self.observer, date=self.date)

        self.sunrise, self.sunset = s['sunrise'], s['sunset']

    def deg_below_horizon(
        self,
        deg_below_horizon: float,
        sun_event: SunEvent,
    ) -> datetime:
        """Get the time for the sun at a certain degrees above / below horizon.

        Args:
            deg_below_horizon: The degrees above / below horizon.
            sun_event: The sun event (sunrise or sunset).

        Returns:
            The time in UTC.
        """
        direction: SunDirection = (
            SunDirection.RISING if sun_event is SunEvent.RISE else SunDirection.SETTING
        )

        return time_at_elevation(self.observer, deg_below_horizon, self.date, direction)
