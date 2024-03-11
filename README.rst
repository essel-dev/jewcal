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

Convert Gregorian to Jewish dates and get Shabbos / Yom Tov details for Diaspora and Israel.

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

  Today is 18 Cheshvan 5784

  JewCal(year=5784, month=8, day=18, gregorian_date=datetime.date(2023, 11, 2),
  shabbos=None, yomtov=None, category=None, diaspora=True)


.. include_quickstart_end


The code for this quickstart is available here: `<src/jewcal/__main__.py>`_.


Resources
---------

- `JewCal @ PyPI <https://pypi.org/project/jewcal/>`_
- `JewCal @ Read the Docs <https://jewcal.readthedocs.io/>`_
