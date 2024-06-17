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
.. image:: https://readthedocs.org/projects/jewcal/badge/?version=stable
    :target: https://jewcal.readthedocs.io/en/stable/?badge=stable
    :alt: Documentation Status

|



.. include_intro_start

Convert Gregorian to Jewish dates with holidays for Diaspora and Israel.

Get info about:

* The Jewish date
* Shabbos and Yom Tov events
* The action (`Candles` or `Havdalah`)


Determine whether it is:

* Erev Shabbos or Erev Yom Tov
* Shabbos
* Yom Tov
* Issur Melacha


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
    diaspora=True
  )


.. include_quickstart_end


Resources
---------

- `JewCal @ PyPI <https://pypi.org/project/jewcal/>`_
- `JewCal @ Read the Docs <https://jewcal.readthedocs.io/>`_
