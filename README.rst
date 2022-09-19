.. include_title_start

JewCal
======

.. include_title_end

.. image:: https://github.com/essel-dev/jewcal/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/essel-dev/jewcal/actions/workflows/tests.yml
    :alt: Tests Status

.. image:: https://github.com/essel-dev/jewcal/actions/workflows/pypi.yml/badge.svg
    :target: https://github.com/essel-dev/jewcal/actions/workflows/pypi.yml
    :alt: PyPi Status

.. image:: https://readthedocs.org/projects/jewcal/badge/?version=latest
    :target: https://jewcal.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

|

.. include_intro_start

A Jewish Calendar with holidays and fasts.

- Convert Gregorian to Jewish dates.
- Determine whether it is *(Erev) Shabbat, (Erev) Yom Tov, Issur Melacha*, ... .
- For Israel and Diaspora.
- Ideal for home automation (e.g. `Home Assistant
  <https://www.home-assistant.io/>`_ with `AppDaemon
  <https://github.com/AppDaemon/appdaemon>`_).

.. include_intro_end


.. include_quickstart_start

Installation
------------

.. code-block:: bash

  pip install jewcal


Quickstart
----------

Run in the console:

.. code-block:: bash

  jewcal


The output:

.. code-block:: console

  Today is 23 Elul 5782 (2022-09-19)
  It is Erev Shabbat: False
  It is Erev Yom Tov: False
  It is Shabbat: False
  It is Yom Tov: False
  It is Issur Melacha: False

  Yesterday was 22 Elul 5782 (2022-09-18)
  Tomorrow is 24 Elul 5782 (2022-09-20)

  Past week:
  15 Elul 5782 (2022-09-11)
  16 Elul 5782 (2022-09-12)
  17 Elul 5782 (2022-09-13)
  18 Elul 5782 (2022-09-14)
  19 Elul 5782 (2022-09-15)
  20 Elul 5782 (2022-09-16) Erev Shabbat
  21 Elul 5782 (2022-09-17) Shabbat

  Current week:
  22 Elul 5782 (2022-09-18)
  23 Elul 5782 (2022-09-19)
  24 Elul 5782 (2022-09-20)
  25 Elul 5782 (2022-09-21)
  26 Elul 5782 (2022-09-22)
  27 Elul 5782 (2022-09-23) Erev Shabbat
  28 Elul 5782 (2022-09-24) Shabbat

  Next 2 weeks:
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


The code:

.. code-block:: python

  jewcal = JewCal()

  print(f'Today is {jewcal.day}.')

  print(f'It is Erev Shabbat: {jewcal.day.is_erev_shabbat()}')
  print(f'It is Erev Yom Tov: {jewcal.day.is_erev_yom_tov()}')
  print(f'It is Shabbat: {jewcal.day.is_shabbat()}')
  print(f'It is Yom Tov: {jewcal.day.is_yom_tov()}')
  print(f'It is Issur Melacha: {jewcal.day.is_issur_melacha()}')

  print(f'\nYesterday was {jewcal.days(-1)[0]}')
  print(f'Tomorrow is {jewcal.days(1)[0]}')

  print('\nPast week:')
  for day in jewcal.weeks(-1):
      print(day)

  print('\nCurrent week:')
  for day in jewcal.current_week():
      print(day)

  print('\nNext 2 weeks:')
  for day in jewcal.weeks(2):
      print(day)

.. include_quickstart_end

.. include_resources_start

Resources
---------

- `JewCal @ PyPI <https://pypi.org/project/jewcal/>`_
- `JewCal @ Read the Docs <https://jewcal.readthedocs.io/>`_
