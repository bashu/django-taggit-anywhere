Changes
-------

2.1.1 (2026-11-13)
~~~~~~~~~~~~~~~~~~

* Switched build backend from setuptools to hatchling.
* Moved package to ``src/`` layout; tests moved to top-level ``tests/``.
* Ported tests to pytest-django fixtures.
* Removed the ``example`` project, the empty ``locale`` directory and empty ``models.py`` modules.
* Removed unused mypy, django-stubs, djLint and factory-boy dev dependencies.

2.1.0 (2026-10-10)
~~~~~~~~~~~~~~~~~~

* Dropped Python < 3.11 support; 3.11 is now the minimum requirement.
* Added Python 3.15 support.

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
