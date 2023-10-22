Jewcal
------
.. image:: https://github.com/essel-dev/jewcal/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/essel-dev/jewcal/actions/workflows/tests.yml
    :alt: Tests Status

.. image:: https://github.com/essel-dev/jewcal/actions/workflows/pypi.yml/badge.svg
    :target: https://github.com/essel-dev/jewcal/actions/workflows/pypi.yml
    :alt: PyPi Status

|

Convert Gregorian to Jewish dates and get Shabbos / Yom Tov details for Diaspora and Israel.

Installation
------------
.. code-block:: bash

  pip install jewcal

Usage
-----

Diaspora
~~~~~~~~

.. code-block:: python

  >>> from datetime import date
  >>> from jewcal import Jewcal

  >>> jewcal = Jewcal(date(2022, 4, 17))
  >>> print(jewcal)
  16 Nisan 5782
  >>> print(repr(jewcal))
  Jewcal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17),
  shabbos=None, yomtov='Pesach 2', category='Havdalah', diaspora=True)


Israel
~~~~~~

.. code-block:: python

  >>> from datetime import date
  >>> from jewcal import Jewcal

  >>> jewcal = Jewcal(date(2022, 4, 17), diaspora=False)
  >>> print(jewcal)
  16 Nisan 5782
  >>> print(repr(jewcal))
  Jewcal(year=5782, month=1, day=16, gregorian_date=datetime.date(2022, 4, 17),
  shabbos=None, yomtov='Chol HaMoed 1 (Pesach 2)', category=None, diaspora=False)



Possible values
---------------

Shabbos
~~~~~~~

+---------------------+----------------------+
| ``jewcal.shabbos``  | ``jewcal.category``  |
+=====================+======================+
| ``None``            | ``None``             |
+---------------------+----------------------+
| Erev Shabbos        | Candles              |
+---------------------+----------------------+
| Shabbos             | Havdalah             |
+---------------------+----------------------+


Yom Tov
~~~~~~~

Diaspora
++++++++

+---------------------------+----------------------+
|``jewcal.yomtov``          | ``jewcal.category``  |
+===========================+======================+
| ``None``                  | ``None``             |
+---------------------------+----------------------+
| Erev Rosh Hashana         | Candles              |
+---------------------------+----------------------+
| Rosh Hashana 1            | Candles              |
+---------------------------+----------------------+
| Rosh Hashana 2            | Havdalah             |
+---------------------------+----------------------+
| Erev Yom Kippur           | Candles              |
+---------------------------+----------------------+
| Yom Kippur                | Havdalah             |
+---------------------------+----------------------+
| Erev Sukkos               | Candles              |
+---------------------------+----------------------+
| Sukkos 1                  | Candles              |
+---------------------------+----------------------+
| Sukkos 2                  | Havdalah             |
+---------------------------+----------------------+
| Chol HaMoed 1 (Sukkos 3)  | ``None``             |
+---------------------------+----------------------+
| Chol HaMoed 2 (Sukkos 4)  | ``None``             |
+---------------------------+----------------------+
| Chol HaMoed 3 (Sukkos 5)  | ``None``             |
+---------------------------+----------------------+
| Chol HaMoed 4 (Sukkos 6)  | ``None``             |
+---------------------------+----------------------+
| Hoshana Rabba (Sukkos 7)  | Candles              |
+---------------------------+----------------------+
| Shmini Atzeres (Sukkos 8) | Candles              |
+---------------------------+----------------------+
| Simchas Tora              | Havdalah             |
+---------------------------+----------------------+
| Erev Pesach               | Candles              |
+---------------------------+----------------------+
| Pesach 1                  | Candles              |
+---------------------------+----------------------+
| Pesach 2                  | Havdalah             |
+---------------------------+----------------------+
| Chol HaMoed 1 (Pesach 3)  | ``None``             |
+---------------------------+----------------------+
| Chol HaMoed 2 (Pesach 4)  | ``None``             |
+---------------------------+----------------------+
| Chol HaMoed 3 (Pesach 5)  | ``None``             |
+---------------------------+----------------------+
| Chol HaMoed 4 (Pesach 6)  | Candles              |
+---------------------------+----------------------+
| Pesach 7                  | Candles              |
+---------------------------+----------------------+
| Pesach 8                  | Havdalah             |
+---------------------------+----------------------+
| Erev Shavuos              | Candles              |
+---------------------------+----------------------+
| Shavuos 1                 | Candles              |
+---------------------------+----------------------+
| Shavuos 2                 | Havdalah             |
+---------------------------+----------------------+


Israel
++++++++

+-------------------------------+----------------------+
|``jewcal.yomtov``              |``jewcal.category``   |
+===============================+======================+
| ``None``                      | ``None``             |
+-------------------------------+----------------------+
| Erev Rosh Hashana             | Candles              |
+-------------------------------+----------------------+
| Rosh Hashana 1                | Candles              |
+-------------------------------+----------------------+
| Rosh Hashana 2                | Havdalah             |
+-------------------------------+----------------------+
| Erev Yom Kippur               | Candles              |
+-------------------------------+----------------------+
| Yom Kippur                    | Havdalah             |
+-------------------------------+----------------------+
| Erev Sukkot                   | Candles              |
+-------------------------------+----------------------+
| Sukkot 1                      | Havdalah             |
+-------------------------------+----------------------+
| Chol HaMoed 1 (Sukkot 2)      | ``None``             |
+-------------------------------+----------------------+
| Chol HaMoed 2 (Sukkot 3)      | ``None``             |
+-------------------------------+----------------------+
| Chol HaMoed 3 (Sukkot 4)      | ``None``             |
+-------------------------------+----------------------+
| Chol HaMoed 4 (Sukkot 5)      | ``None``             |
+-------------------------------+----------------------+
| Chol HaMoed 5 (Sukkot 6)      | ``None``             |
+-------------------------------+----------------------+
| Hoshana Rabba (Sukkot 7)      | Candles              |
+-------------------------------+----------------------+
| Shmini Atzeret / Simchat Tora | Havdalah             |
+-------------------------------+----------------------+
| Erev Pesach                   | Candles              |
+-------------------------------+----------------------+
| Pesach 1                      | Havdalah             |
+-------------------------------+----------------------+
| Chol HaMoed 1 (Pesach 2)      | ``None``             |
+-------------------------------+----------------------+
| Chol HaMoed 2 (Pesach 3)      | ``None``             |
+-------------------------------+----------------------+
| Chol HaMoed 3 (Pesach 4)      | ``None``             |
+-------------------------------+----------------------+
| Chol HaMoed 4 (Pesach 5)      | ``None``             |
+-------------------------------+----------------------+
| Chol HaMoed 5 (Pesach 6)      | Candles              |
+-------------------------------+----------------------+
| Pesach 7                      | Havdalah             |
+-------------------------------+----------------------+
| Erev Shavuot                  | Candles              |
+-------------------------------+----------------------+
| Shavuot                       | Havdalah             |
+-------------------------------+----------------------+
