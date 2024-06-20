"""Zmanim model."""

from dataclasses import InitVar, dataclass, field
from datetime import date, datetime, timedelta
from typing import Final

from jewcal.helpers.sun import Sun, SunEvent
from jewcal.utils.datetime import date_today, datetime_now

HALACHIC_HOURS: Final[int] = 12
PLAG_HAMINCHA: Final[float] = 10.75
TZEIS_HAKOCHAVIM: Final[float] = 8.5


@dataclass
class Location:
    """Location and Zmanim configuration."""

    latitude: float
    """The latitude of the location."""

    longitude: float
    """The longitude of the location."""

    use_tzeis_hakochavim: bool = field(default=True)
    """Use Tzeis Hakochavim or Tzeis at minutes after sunset for nightfall.

    `True` to use :py:class:`Zmanim.hadlokas_haneiros`, `False` to use
    :py:class:`Zmanim.tzeis_minutes`.
    """

    hadlokas_haneiros_minutes: int = field(default=18)
    """Hadlokas Haneiros at minutes before sunset."""

    tzeis_minutes: int = field(default=72)
    """Tzeis at minutes after sunset."""


@dataclass
class Zmanim:
    """The zmanim of the day."""

    gregorian_date: InitVar[date]
    """The date to calculate the Zmanim for."""

    location: InitVar[Location]
    """The location to calculate the Zmanim for."""

    set_hadlokas_haneiros: InitVar[bool] = False
    """`True` to set :py:attr:`hadlokas_haneiros`, `False` otherwise."""

    sunrise: datetime = field(init=False)
    """0.833 degrees above horizon."""

    sunset: datetime = field(init=False)
    """0.833 degrees below horizon"""

    plag_hamincha: datetime = field(init=False)
    """Sunrise plus 10.75 halachic hours."""

    hadlokas_haneiros: datetime | None = field(init=False, default=None)
    """Hadlokas Haneiros at minutes before sunset."""

    tzeis_hakochavim: datetime = field(init=False)
    """Nightfall at 8.5 degrees below the horizon."""

    tzeis_minutes: datetime = field(init=False)
    """Nightfall at minutes after sunset."""

    def __post_init__(
        self,
        gregorian_date: date,
        location: Location,
        set_hadlokas_haneiros: bool,
    ) -> None:
        """Post init.

        Args:
            gregorian_date: The date to calculate the Zmanim for.
            location: The location to calculate the Zmanim for.
            set_hadlokas_haneiros: `True` to set :py:attr:`hadlokas_haneiros`, `False`
                otherwise.
        """
        self.set_zmanim(
            gregorian_date,
            location,
            set_hadlokas_haneiros=set_hadlokas_haneiros,
        )

    def to_dict(self) -> dict[str, str | None]:
        """Get the zmanim as a dictionary.

        Returns:
            A dictionary representation of the zmanim in UTC.
        """
        hadlokas_haneiros = (
            self.hadlokas_haneiros.isoformat() if self.hadlokas_haneiros else None
        )

        return {
            'sunrise': self.sunrise.isoformat(),
            'sunset': self.sunset.isoformat(),
            'plag_hamincha': self.plag_hamincha.isoformat(),
            'hadlokas_haneiros': hadlokas_haneiros,
            'tzeis_hakochavim': self.tzeis_hakochavim.isoformat(),
            'tzeis_minutes': self.tzeis_minutes.isoformat(),
        }

    def set_zmanim(
        self,
        gregorian_date: date,
        location: Location,
        *,
        set_hadlokas_haneiros: bool = False,
    ) -> None:
        """Set the zmanim.

        Args:
            gregorian_date: The date of the zmanim.
            location: The location to calculate the Zmanim for.
            set_hadlokas_haneiros: `True` to set :py:attr:`hadlokas_haneiros`, `False`
                otherwise.
        """
        lat, lon = location.latitude, location.longitude

        sun = Sun(gregorian_date, lat, lon)
        sunrise, sunset = sun.sunrise, sun.sunset

        tzeis_hakochavim = sun.deg_below_horizon(TZEIS_HAKOCHAVIM, SunEvent.SET)
        tzeis_minutes = sunset + timedelta(minutes=location.tzeis_minutes)

        halachic_hour = (sunset - sunrise) / HALACHIC_HOURS
        plag = sunrise + halachic_hour * PLAG_HAMINCHA

        neiros = None
        if set_hadlokas_haneiros:
            neiros = sunset - timedelta(minutes=location.hadlokas_haneiros_minutes)

        self.sunrise = sunrise
        self.sunset = sunset
        self.plag_hamincha = plag
        self.hadlokas_haneiros = neiros
        self.tzeis_hakochavim = tzeis_hakochavim
        self.tzeis_minutes = tzeis_minutes

    def is_now_after_nightfall(self, *, use_tzeis_hakochavim: bool) -> bool:
        """Is now after nightfall.

        If the date is today, check if `datetime.now` is after nightfall.

        Args:
            use_tzeis_hakochavim: `True` to use :py:attr:`tzeis_hakochavim`, `False`
                to use :py:attr:`tzeis_minutes` for nightfall.

        Returns:
            `True` is it after nightfall, `False` otherwise.
        """
        nightfall_time = (
            self.tzeis_hakochavim if use_tzeis_hakochavim else self.tzeis_minutes
        )

        return bool(
            nightfall_time.date() == date_today() and datetime_now() > nightfall_time,
        )
