"""Package jewcal."""

from sys import modules
from types import ModuleType
from typing import cast
from warnings import warn

from .core import JewCal

Jewcal = JewCal


class Wrapper:  # pylint: disable=too-few-public-methods
    """Rename class `Jewcal` to `JewCal`."""

    def __init__(self, wrapped: ModuleType):
        self.wrapped: ModuleType = wrapped

    def __getattr__(self, name: str) -> ModuleType:
        if name == 'Jewcal':
            # DeprecationWarning does not alert the user if not in
            # development mode
            warn('Class Jewcal is deprecated and renamed to JewCal')

        return cast(ModuleType, getattr(self.wrapped, name))


modules[__name__] = cast(ModuleType, Wrapper(modules[__name__]))


__all__ = [
    'JewCal',
]
