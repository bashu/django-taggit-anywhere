django-taggit-anywhere
======================

Even more simpler approach to tagging with
django-taggit_. Additionally this project provides easy-to-use
integration with django-taggit-helpers_ and django-taggit-labels_

.. image:: https://img.shields.io/pypi/v/django-taggit-anywhere.svg
    :target: https://pypi.python.org/pypi/django-taggit-anywhere/

.. image:: https://img.shields.io/pypi/dm/django-taggit-anywhere.svg
    :target: https://pypi.python.org/pypi/django-taggit-anywhere/

.. image:: https://img.shields.io/github/license/bashu/django-taggit-anywhere.svg
    :target: https://pypi.python.org/pypi/django-taggit-anywhere/

Requirements
------------

You must have *django-taggit* installed and configured, see the django-taggit_ documentation for details and setup instructions.

Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install django-taggit-anywhere

Setup
=====

Make sure the project is configured for django-taggit_.

You'll need to add ``taggit_anywhere`` as a **LAST** item to ``INSTALLED_APPS`` in your project's ``settings.py`` file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        # optional integration with django-taggit-helpers
        'taggit_helpers',  # pip install django-taggit-helpers

        # optional integration with django-taggit-labels
        'taggit_labels',  # pip install django-taggit-labels

        'taggit_anywhere',  # must be last in a list
    )

There is only one mandatory configuration option you need to set in your ``settings.py``:

.. code-block:: python

    TAGGIT_FOR_MODELS = [
        '<app_name>.<model_name>',
    ]


Please see ``example`` application. This application is used to manually test the functionalities of this package. This also serves as good example...

You need Django 1.8 or above to run that. It might run on older versions but that is not tested.

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-taggit: https://github.com/alex/django-taggit
.. _django-taggit-helpers: https://github.com/mfcovington/django-taggit-helpers
.. _django-taggit-labels: https://github.com/bennylope/django-taggit-labels
