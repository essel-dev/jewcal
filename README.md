# Jewcal
[![Tests](https://github.com/essel-dev/jewcal/actions/workflows/tests.yml/badge.svg)](https://github.com/essel-dev/jewcal/actions/workflows/tests.yml) [![PyPi](https://github.com/essel-dev/jewcal/actions/workflows/pypi.yml/badge.svg)](https://github.com/essel-dev/jewcal/actions/workflows/pypi.yml)

Convert Gregorian to Jewish dates and get shabbos / yom tov details for Diaspora.

## Installation
```sh
pip install jewcal
```

## Usage
```py
>>> from datetime import date
>>> from jewcal import Jewcal

>>> jewcal = Jewcal(date(2022, 4, 15))
>>> print(jewcal)
14 Nisan 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=1, day=14, gregorian_date=datetime.date(2022, 4, 15), shabbos='Erev Shabbos', yomtov='Erev Pesach', category='Candles')

>>> jewcal = Jewcal(date(2022, 4, 16))
>>> print(jewcal)
15 Nisan 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=1, day=15, gregorian_date=datetime.date(2022, 4, 16), shabbos='Shabbos', yomtov='Pesach 1', category='Candles')

>>> jewcal = Jewcal(date(2022, 4, 17))
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17), shabbos=None, yomtov='Pesach 2', category='Havdalah')

>>> jewcal = Jewcal(date(2022, 8, 19))
>>> print(jewcal)
22 Av 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=5, day=22, gregorian_date=datetime.date(2022, 8, 19), shabbos='Erev Shabbos', yomtov=None, category='Candles')

>>> jewcal = Jewcal(date(2022, 8, 20))
>>> print(jewcal)
23 Av 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=5, day=23, gregorian_date=datetime.date(2022, 8, 20), shabbos='Shabbos', yomtov=None, category='Havdalah')

>>> jewcal = Jewcal(date.today())
>>> print(jewcal)
24 Av 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=5, day=24, gregorian_date=datetime.date(2022, 8, 21), shabbos=None, yomtov=None, category=None)
```

## Possible values
### Shabbos
|`jewcal.shabbos`|`jewcal.category`|
| :--- | :--- |
|	`None`	|	`None`	|
|	Erev Shabbos	|	Candles	|
|	Shabbos	|	Havdalah	|

### Yom Tov
|`jewcal.yomtov`|`jewcal.category`|
| :--- | :--- |
|	`None`	|	`None`	|
| Erev Rosh Hashana	|	Candles	|
|	Rosh Hashana 1	|	Candles	|
|	Rosh Hashana 2	|	Havdalah	|
|	Erev Yom Kippur	|	Candles	|
|	Yom Kippur	|	Havdalah	|
|	Erev Sukkos	|	Candles	|
|	Sukkos 1	|	Candles	|
|	Sukkos 2	|	Havdalah	|
|	Chol HaMoed 1 (Sukkos 3)  |	`None`	|
|	Chol HaMoed 2 (Sukkos 4)  |	`None`	|
|	Chol HaMoed 3 (Sukkos 5)  |	`None`	|
|	Chol HaMoed 4 (Sukkos 6)  |	`None`	|
|	Hoshana Rabba (Sukkos 7) |	Candles	|
|	Shmini Atzeres (Sukkos 8) |	Candles	|
|	Simchas Tora	|	Havdalah	|
|	Erev Pesach	|	Candles	|
|	Pesach 1  |	Candles	|
|	Pesach 2	|	Havdalah	|
|	Chol HaMoed 1 (Pesach 3)  |	`None`	|
|	Chol HaMoed 2 (Pesach 4)  |	`None`	|
|	Chol HaMoed 3 (Pesach 5)  |	`None`	|
|	Chol HaMoed 4 (Pesach 6)  |	Candles	|
|	Pesach 7	|	Candles	|
|	Pesach 8	|	Havdalah	|
|	Erev Shavuos	|	Candles	|
|	Shavuos 1	|	Candles	|
|	Shavuos 2	|	Havdalah	|
