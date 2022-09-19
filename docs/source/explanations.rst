Design decisions
================

JewCal caches generated calendars upon creation.

This optimization is noticeable when creating many Jewish dates in a
single run.

In that case it is recommended to set the current date on an existing
JewCal-instance rather than creating new ones.

.. topic:: Tutorial

  :ref:`Set the current day`
