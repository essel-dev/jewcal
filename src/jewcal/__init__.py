"""JewCal examples of usage.

Initialize JewCal
-----------------

>>> # Diaspora
>>> jewcal = JewCal()  # today's date
>>> jewcal = JewCal(date(2022, 4, 16))  # specific date
>>>
>>> # Israel
>>> jewcal = JewCal(diaspora=False)  # today's date
>>> jewcal = JewCal(date(2022, 4, 16), False)  # specific date


Is it ...
-----------

>>> jewcal = JewCal(date(2022, 9, 23))
>>> print(jewcal.day)
27 Elul 5782 (2022-09-23) Erev Shabbat
>>>
>>> jewcal.day.is_holiday()
False
>>> jewcal.day.is_fast_day()
False
>>> jewcal.day.is_erev_shabbat()
True
>>> jewcal.day.is_shabbat()
False
>>> jewcal.day.is_erev_yomtov()
False
>>> jewcal.day.is_yomtov()
False
>>> jewcal.day.is_issur_melacha()
False
>>> jewcal.day.is_chag()
False


Get/Set current day
---------------------

>>> jewcal = JewCal(date(2022, 9, 23))
>>>
>>> # get
>>> print(jewcal.day)
27 Elul 5782 (2022-09-23) Erev Shabbat
>>>
>>> # set
>>> jewcal.date(date(2050, 1, 1))
>>> print(jewcal.day)
7 Tevet 5810 (2050-01-01) Shabbat


Get (active) day categories
-------------------------------
>>> jewcal = JewCal(date(2022, 9, 23))
>>>
>>> # Get all categories with True or False values.
>>> for category in jewcal.day.categories:
...    category
('erev', True)
('shabbat', False)
('yomtov', False)
('chag', False)
('fast', False)
>>>
>>> # Get all categories that are True.
>>> jewcal.day.active_categories()
['erev']


Get holiday/fast names
-------------------------------
>>> jewcal = JewCal(date(2022, 9, 23))
>>>
>>> jewcal.day.names
['Erev Shabbat']


Get current/past/future days or weeks
-------------------------------------
>>> jewcal = JewCal(date(2022, 9, 23))
>>>
>>> # current day
>>> print(jewcal.day)
27 Elul 5782 (2022-09-23) Erev Shabbat
>>>
>>> # yesterday
>>> for day in jewcal.days(-1):
...    print(day)
26 Elul 5782 (2022-09-22)
>>>
>>> # next 2 days
>>> for day in jewcal.days(2):
...    print(day)
28 Elul 5782 (2022-09-24) Shabbat
29 Elul 5782 (2022-09-25) Erev Rosh Hashana
>>>
>>> # current week
>>> for day in jewcal.current_week():
...    print(day)
22 Elul 5782 (2022-09-18)
23 Elul 5782 (2022-09-19)
24 Elul 5782 (2022-09-20)
25 Elul 5782 (2022-09-21)
26 Elul 5782 (2022-09-22)
27 Elul 5782 (2022-09-23) Erev Shabbat
28 Elul 5782 (2022-09-24) Shabbat
>>>
>>> # last week
>>> for day in jewcal.weeks(-1):
...    print(day)
15 Elul 5782 (2022-09-11)
16 Elul 5782 (2022-09-12)
17 Elul 5782 (2022-09-13)
18 Elul 5782 (2022-09-14)
19 Elul 5782 (2022-09-15)
20 Elul 5782 (2022-09-16) Erev Shabbat
21 Elul 5782 (2022-09-17) Shabbat
>>>
>>> # next 3 weeks
>>> for day in jewcal.weeks(3):
...    print(day)
29 Elul 5782 (2022-09-25) Erev Rosh Hashana
1 Tishrei 5783 (2022-09-26) Rosh Hashana 1
2 Tishrei 5783 (2022-09-27) Rosh Hashana 2
3 Tishrei 5783 (2022-09-28) Tzom Gedalia
4 Tishrei 5783 (2022-09-29)
5 Tishrei 5783 (2022-09-30) Erev Shabbat
6 Tishrei 5783 (2022-10-01) Shabbat
7 Tishrei 5783 (2022-10-02)
8 Tishrei 5783 (2022-10-03)
9 Tishrei 5783 (2022-10-04) Erev Yom Kippur
10 Tishrei 5783 (2022-10-05) Yom Kippur
11 Tishrei 5783 (2022-10-06)
12 Tishrei 5783 (2022-10-07) Erev Shabbat
13 Tishrei 5783 (2022-10-08) Shabbat
14 Tishrei 5783 (2022-10-09) Erev Sukkot
15 Tishrei 5783 (2022-10-10) Sukkot 1
16 Tishrei 5783 (2022-10-11) Sukkot 2
17 Tishrei 5783 (2022-10-12) Sukkot Chol HaMoed 1
18 Tishrei 5783 (2022-10-13) Sukkot Chol HaMoed 2
19 Tishrei 5783 (2022-10-14) Erev Shabbat, Sukkot Chol HaMoed 3
20 Tishrei 5783 (2022-10-15) Shabbat, Sukkot Chol HaMoed 4
"""

from datetime import date  # noqa: F401

from .core import JewCal

__all__ = (
    'JewCal',
)
