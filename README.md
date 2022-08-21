# jewcal
[![Tests](https://github.com/essel-dev/jewcal/actions/workflows/python-app.yml/badge.svg)](https://github.com/essel-dev/jewcal/actions/workflows/python-app.yml)

Convert Gregorian dates to Jewish dates and get Shabbos / holiday details for Diaspora.

## Installation
```sh
pip install jewcal
```

## Usage
```py
>>> from datetime import date
>>> from jewcal import Jewcal

>>> jewcal = Jewcal(date.today())
>>> print(jewcal)
24 Av 5782
>>> print(repr(jewcal))
Jewcal(year=5782, month=5, day=24, shabbos=None, holiday=None, category=None)

>>> jewcal2 = Jewcal(date(2022, 8, 19))
>>> print(jewcal2)
22 Av 5782
>>> print(repr(jewcal2))
Jewcal(year=5782, month=5, day=22, shabbos='Erev Shabbos', holiday=None, category=<Category.CANDLES: 'Candles'>)
```

## Possible values
|	Shabbos / holiday	|	Category	|
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
