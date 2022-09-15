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

.. .. image:: https://readthedocs.org/projects/jewcal/badge/?version=latest
..     :target: https://jewcal.readthedocs.io/en/latest/?badge=latest
..     :alt: Documentation Status

|

.. include_start_intro

JewCal is a Jewish Calendar with holidays and fasts.

One of the advantages of JewCal is using Boolean values to deduce if it is
Shabbat or Yom Tov.

The aim of JewCal is using it in other projects like
`Home Assistant <https://www.home-assistant.io/>`_ with
`AppDaemon <https://github.com/AppDaemon/appdaemon>`_ for home automation.

.. include_end_intro

.. include_start_install

Installing
----------
.. code-block:: bash

  pip install jewcal

A Simple Example
----------------

Run in the console:

.. code-block:: bash

  jewcal


The output:

.. code-block:: console

  Today is 19 Elul 5782 (2022-09-15).

  Day(
    date=Date(
      gregorian=datetime.date(2022, 9, 15),
      year=5782,
      month=6,
      day=19,
      weekday=4
    ),
    erev=False,
    shabbat=False,
    yom_tov=False,
    chol_hamoed=False,
    chag=False,
    rosh_chodesh=False,
    fast=False,
    names=[]
  )


The code:

.. code-block:: python

  jewcal = JewCal()

  print(f'Today is {jewcal.day}\n')

  print(repr(jewcal.day))

.. include_end_install

Resources
---------
- Documentation: https://jewcal.readthedocs.io/
- PyPI: https://pypi.org/project/jewcal/