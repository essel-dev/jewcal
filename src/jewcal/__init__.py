"""JewCal usage examples.

Diaspora
--------

>>> jewcal = JewCal(date.today())  # today's date

>>> jewcal = JewCal(date(2022, 4, 17))  # specific date
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
JewCal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17),
shabbos=None, yomtov='Pesach 2', category='Havdalah', diaspora=True)


Israel
------

>>> jewcal = JewCal(date.today(), diaspora=False)  # today's date

>>> jewcal = JewCal(date(2022, 4, 17), diaspora=False)  # specific date
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
JewCal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17),
shabbos=None, yomtov='Chol HaMoed 1 (Pesach 2)', category=None, diaspora=False)
"""

from datetime import date  # noqa: F401

from .core import Jewcal  # noqa: F401  # deprecated
from .core import JewCal

__all__ = [
    'Jewcal',
    'JewCal',
]
