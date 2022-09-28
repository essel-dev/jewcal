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

JewCal is a Jewish Calendar with holidays and fasts for Israel and Diaspora.

You can convert Gregorian to Jewish dates and determine whether a day is
*(Erev) Shabbat, (Erev) Yom Tov, Issur Melacha* and more.

JewCal is mainly developed for use with home automation
(e.g. `Home Assistant <https://www.home-assistant.io/>`_ with `AppDaemon
<https://github.com/AppDaemon/appdaemon>`_).

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

  Today is 27 Elul 5782 (2022-09-23) Erev Shabbat
  Is Erev Shabbat: True
  Is Shabbat: False
  Is Erev Yom Tov: False
  Is Yom Tov: False
  Is Issur Melacha: False

.. include_quickstart_end

The code for this quickstart is available here: `<src/jewcal/__main__.py>`_.

.. include_resources_start

Resources
---------

- `JewCal @ PyPI <https://pypi.org/project/jewcal/>`_
- `JewCal @ Read the Docs <https://jewcal.readthedocs.io/>`_
