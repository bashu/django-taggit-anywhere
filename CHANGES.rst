Changes
-------

2.0.0 (2026-08-14)
~~~~~~~~~~~~~~~~~~

* Dropped Python < 3.10 support; now tested on Python 3.10-3.14.
* Dropped Django < 5.2 support; now tested on Django 5.2, 6.0 and 6.1.
* Fixed ``AppConfig.ready()``'s "already tagged" guard, which was unreachable
  dead code and would raise ``ValueError`` if ``ready()`` ever ran twice.

1.0.0 (2021-11-29)
~~~~~~~~~~~~~~~~~~

* Added Django 3+ support.
* Dropped Python 2.7 support.
* Dropped Django 1.10 / 1.11 support.
