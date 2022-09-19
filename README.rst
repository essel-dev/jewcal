.. include_start_title

JewCal - Jewish Calendar
=========================

.. include_end_title

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

.. include_start_intro

JewCal is a Jewish Calendar for Diaspora and Israel with holidays and fasts.

These holidays occur on the same dates every year, but the dates vary in the
Gregorian calendar. JewCal makes it possible to convert Gregorian to Jewish
dates and to get the holiday and fast details.

One of the advantages of JewCal is using Boolean functions to deduce if it is
*(Erev) Shabbat* or *Yom Tov* and if it is *Issur Melacha*.

The aim of JewCal is using it in other projects like
`Home Assistant <https://www.home-assistant.io/>`_ with
`AppDaemon <https://github.com/AppDaemon/appdaemon>`_ for home automation.

.. include_end_intro

.. include_start_install

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

  Today is 14 Nisan 5782 (2022-04-15) Erev Shabbat, Erev Pesach.

  It is Erev Shabbat: True
  It is Erev Yom Tov: True

  It is Shabbat: False
  It is Yom Tov: False

  It is Issur Melacha: False


The code:

.. code-block:: python

  jewcal = JewCal()

  print(f'Today is {jewcal.day}.')

  print(f'It is Erev Shabbat: {jewcal.day.is_erev_shabbat()}')
  print(f'It is Erev Yom Tov: {jewcal.day.is_erev_yom_tov()}')

  print(f'It is Shabbat: {jewcal.day.is_shabbat()}')
  print(f'It is Yom Tov: {jewcal.day.is_yom_tov()}')

  print(f'It is Issur Melacha: {jewcal.day.is_issur_melacha()}')

.. include_end_install

Resources
---------
- Documentation: https://jewcal.readthedocs.io/
- PyPI: https://pypi.org/project/jewcal/
