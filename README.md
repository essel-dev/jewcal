# jewcal
[![Tests](https://github.com/essel-dev/jewcal/actions/workflows/python-app.yml/badge.svg)](https://github.com/essel-dev/jewcal/actions/workflows/python-app.yml)

Convert Gregorian dates to Jewish dates and get shabbos / yomtov details for Diaspora.

## Installation
```sh
pip install jewcal
```

## Usage
```py
>>> from datetime import date
>>> from jewcal import Jewcal

>>> jewcal = Jewcal(date(2022, 4, 15))
>>> print(repr(jewcal))
Jewcal(year=5782, month=1, day=14, shabbos='Erev Shabbos', yomtov='Erev Pesach', category=<Category.CANDLES: 'Candles'>)

>>> jewcal = Jewcal(date(2022, 4, 16))
>>> print(repr(jewcal))
Jewcal(year=5782, month=1, day=15, shabbos='Shabbos', yomtov='Pesach 1', category=<Category.CANDLES: 'Candles'>)

>>> jewcal = Jewcal(date(2022, 4, 17))
>>> print(jewcal)
16 Nisan 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=1, day=16, shabbos=None, yomtov='Pesach 2', category=<Category.HAVDALAH: 'Havdalah'>)

>>> jewcal = Jewcal(date(2022, 8, 19))
>>> print(jewcal)
22 Av 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=5, day=22, shabbos='Erev Shabbos', yomtov=None, category=<Category.CANDLES: 'Candles'>)

>>> jewcal = Jewcal(date(2022, 8, 20))
>>> print(jewcal)
23 Av 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=5, day=23, shabbos='Shabbos', yomtov=None, category=<Category.HAVDALAH: 'Havdalah'>)

>>> jewcal = Jewcal(date.today())
>>> print(jewcal)
24 Av 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=5, day=24, shabbos=None, yomtov=None, category=None)
```

## Possible values
|	Shabbos / Yomtov	|	Category	|
|	---	|	---	|
|	Erev Shabbos	|	candles	|
|	Shabbos	|	havdalah	|
|	Erev Rosh Hashana	|	candles	|
|	Rosh Hashana 1	|	candles	|
|	Rosh Hashana 2	|	havdalah	|
|	Erev Sukkos	|	candles	|
|	Sukkos 1	|	candles	|
|	Sukkos 2	|	havdalah	|
|	Hoshana Rabba	|	candles	|
|	Shmini Atzeres	|	candles	|
|	Simchas Tora	|	havdalah	|
|	Erev Pesach	|	candles	|
|	Pesach 1	|	candles	|
|	Pesach 2	|	havdalah	|
|	Chol HaMoed Pesach 6	|	candles	|
|	Pesach 7	|	candles	|
|	Pesach 8	|	havdalah	|
|	Erev Shavuos	|	candles	|
|	Shavuos 1	|	candles	|
|	Shavuos 2	|	havdalah	|
