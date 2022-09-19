Tutorials
=========

Calendar
~~~~~~~~

Create a calendar
"""""""""""""""""

.. code-block:: python

  from datetime import date
  from jewcal import JewCal

  # Diaspora
  jewcal = JewCal()  # today's date
  jewcal = JewCal(date(2022, 4, 16))  # specific date

  # Israel
  jewcal = JewCal(False)  # today's date
  jewcal = JewCal(date(2022, 4, 16), False)  # specific date


Day
~~~

Get the current day
"""""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Current day is: {jewcal.day}')


Set the current day
"""""""""""""""""""

.. code-block:: python

  from datetime import date
  from jewcal import JewCal

  jewcal = JewCal()

  jewcal.date(date(2022, 1, 1))

  print(f'Current day is: {jewcal.day}')


Is it a holiday
"""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is a holiday: {jewcal.day.is_holiday()}')


Is it a fast day
""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is a fast day: {jewcal.day.is_fast_day()}')


.. seealso::
  .. automethod:: jewcal.Day.is_fast_day
    :noindex:


Is it Erev Shabbat
""""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is Erev Shabbat: {jewcal.day.is_erev_shabbat()}')


Is it Shabbat
"""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is Shabbat: {jewcal.day.is_shabbat()}')


Is it Erev Yom Tov
""""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is Erev Yom Tov: {jewcal.day.is_erev_yom_tov()}')


Is it Yom Tov
"""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is Yom Tov: {jewcal.day.is_yom_tov()}')


.. seealso::
  .. automethod:: jewcal.Day.is_yom_tov
    :noindex:


Is it Issur Melacha
"""""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Issur Melacha: {jewcal.day.is_issur_melacha()}')


.. seealso::
  .. automethod:: jewcal.Day.is_issur_melacha
    :noindex:


Is it Chol HaMoed
"""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is Chol HaMoed: {jewcal.day.is_chol_hamoed()}')


.. seealso::
  .. automethod:: jewcal.Day.is_chol_hamoed
    :noindex:


Is it a Chag
""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is Chag: {jewcal.day.is_chag()}')


.. seealso::
  .. automethod:: jewcal.Day.is_chag
    :noindex:


Is it Rosh Chodesh
""""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(f'Is Chag: {jewcal.day.is_rosh_chodesh()}')


Get all categories
""""""""""""""""""

Get all categories (holiday and fast) for the current day with ``True`` or
``False`` values:

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  for category, value in jewcal.day.categories:
    print(category, value)


Get all active categories
"""""""""""""""""""""""""

Get all categories (holiday and fast) for the current day that are ``True``:

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(jewcal.day.active_categories())


Get all holiday / fast names
""""""""""""""""""""""""""""

Get all the holiday / fast names for the current day:

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  print(jewcal.day.names)


Get day(s) in the past / future
"""""""""""""""""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  for day in jewcal.days(-1):  # yesterday
    print(day)

  for day in jewcal.days(2):  # next 2 days
    print(day)


Get current week
""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  for day in jewcal.current_week():
    print(day)


Get weeks(s) in the past / future
"""""""""""""""""""""""""""""""""

.. code-block:: python

  from jewcal import JewCal

  jewcal = JewCal()

  for day in jewcal.weeks(-1):  # last week
    print(day)


  for day in jewcal.weeks(3):  # next 3 weeks
    print(day)
