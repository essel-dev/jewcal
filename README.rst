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

.. include_quickstart_end

.. include_resources_start

Resources
---------

- `JewCal @ PyPI <https://pypi.org/project/jewcal/>`_
- `JewCal @ Read the Docs <https://jewcal.readthedocs.io/>`_
