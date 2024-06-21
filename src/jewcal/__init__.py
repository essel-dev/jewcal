"""Package jewcal."""

from sys import modules
from types import ModuleType
from typing import cast
from warnings import warn

from .core import JewCal
from .models.events import Events
from .models.jewish_date import JewishDate, Month
from .models.zmanim import Location, Zmanim

Jewcal = JewCal


class _Wrapper:  # pylint: disable=too-few-public-methods
    """Rename class `Jewcal` to `JewCal`."""

    def __init__(self, wrapped: ModuleType) -> None:
        self.wrapped: ModuleType = wrapped

    def __getattr__(self, name: str) -> ModuleType:
        if name == 'Jewcal':
            # DeprecationWarning does not alert the user if not in
            # development mode
            warn('Jewcal is deprecated, use JewCal', stacklevel=2)

        return cast(ModuleType, getattr(self.wrapped, name))


modules[__name__] = cast(ModuleType, _Wrapper(modules[__name__]))


__all__ = [
    'JewCal',
    'JewishDate',
    'Month',
    'Events',
    'Location',
    'Zmanim',
]
