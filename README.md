# jewcal
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
### Shabbos
|`jewcal.shabbos`|`jewcal.category`|
| :--- | :--- |
|	None	|	None	|
|	Erev Shabbos	|	Candles	|
|	Shabbos	|	Havdalah	|

### Yom Tov
|`jewcal.yomtov`|`jewcal.category`|
| :--- | :--- |
|	None	|	None	|
|	Erev Rosh Hashana	|	Candles	|
|	Rosh Hashana 1	|	Candles	|
|	Rosh Hashana 2	|	Havdalah	|
|	Erev Yom Kippur	|	Candles	|
|	Yom Kippur	|	Havdalah	|
|	Erev Sukkos	|	Candles	|
|	Sukkos 1	|	Candles	|
|	Sukkos 2	|	Havdalah	|
|	Hoshana Rabba	|	Candles	|
|	Shmini Atzeres	|	Candles	|
|	Simchas Tora	|	Havdalah	|
|	Erev Pesach	|	Candles	|
|	Pesach 1	|	Candles	|
|	Pesach 2	|	Havdalah	|
|	Chol HaMoed Pesach 6	|	Candles	|
|	Pesach 7	|	Candles	|
|	Pesach 8	|	Havdalah	|
|	Erev Shavuos	|	Candles	|
|	Shavuos 1	|	Candles	|
|	Shavuos 2	|	Havdalah	|


