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

Convert Gregorian to Jewish dates with holidays and zmanim (Diaspora/Israel).

Get info about:

* The Jewish date
* Shabbos and Yom Tov events
* The action (`Candles` or `Havdalah`)
* The zmanim

  * Sunrise
  * Sunset
  * Plag Hamincha
  * Hadlokas Haneiros (adjust the minutes before sunset)
  * Tzeis (adjust to stars or minutes after sunset)


Determine whether it is:

* Erev Shabbos or Erev Yom Tov
* Shabbos
* Yom Tov
* Issur Melacha

If latitude and longitude are specified, nightfall is taken into account to calculate
the Jewish date.


.. include_intro_end



.. include_quickstart_start

Quickstart
----------

Install with pip:

.. code-block:: bash

  pip install jewcal


Run in the console:

.. code-block:: bash

  jewcal


The output:

.. code-block:: console

  Today is 23 Iyar 5784

  today.has_events()=True
  today.is_erev()=True
  today.is_erev_shabbos()=True
  today.is_shabbos()=False
  today.is_erev_yomtov()=False
  today.is_yomtov()=False
  today.is_issur_melacha()=False

  JewCal(
    jewish_date=JewishDate(
      year=5784, month=2, day=23,
      gregorian_date=datetime.date(2024, 5, 31)
    ),
    events=Events(
      shabbos='Erev Shabbos',
      yomtov=None,
      action='Candles'
    ),
    diaspora=True,
    zmanim=None
  )


  Zmanim for Jerushalayim:
  {
    'hadlokas_haneiros': '2024-05-31T15:59:58.418285+00:00',
    'plag_hamincha': '2024-05-31T15:11:40.067150+00:00',
    'sunrise': '2024-05-31T02:32:14.247357+00:00',
    'sunset': '2024-05-31T16:39:58.418285+00:00',
    'tzeis_hakochavim': '2024-05-31T17:21:58.418285+00:00',
    'tzeis_minutes': '2024-05-31T17:51:58.418285+00:00'
  }

  Location(
    latitude=31.76904, longitude=35.21633,
    use_tzeis_hakochavim=True,
    hadlokas_haneiros_minutes=40,
    tzeis_minutes=72
  )


.. include_quickstart_end


Resources
---------

- `JewCal @ PyPI <https://pypi.org/project/jewcal/>`_
- `JewCal @ Read the Docs <https://jewcal.readthedocs.io/>`_
