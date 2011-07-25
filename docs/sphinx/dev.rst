=====================
Developer conventions
=====================


Quick start
===========

If you have a Linux or OS X system already capable of running Plone then a quick start with collective.table is as follows:

.. sourcecode:: bash

    $ git co git@github.com:nzupan/collective.table.git
    $ cd collective.table/
    $ virtualenv -p python2.6 --no-site-packages ./
    $ bin/python bootstrap.py
    $ bin/buildout

    # start Zope
    $ bin/instance fg


Commit checklist
================

Before every commit you must:

- run all :ref:`unit-tests`.
- perform :ref:`syntax-validation`.
- add an entry to :ref:`changelog` (if applicable).
- add an entry to :ref:`sphinx-docs` (if applicable).

You can run all syntax check and all test with a single command:

.. sourcecode:: bash

    $ ./pre-commit-check.sh

.. _unit-tests:

Unit tests
==========

Un-tested code is broken code.

For every feature you add to the codebase you must also add tests for it.

You can run tests like this:

.. sourcecode:: bash

    $ bin/test -s collective.table


.. _syntax-validation:

Syntax validation
=================

All Python source code should be `PEP-8` valid and checked for syntax errors.
Tools for checking this are `pep8` and `pyflakes`.

If possible make your editor run `pep8` and `pyflakes` on your current
file every time you save it. Useful links:

- http://github.com/ppierre/python-pep8-tmbundle
- http://www.arthurkoziel.com/2008/06/28/pyflakes-installation-and-textmate-integration/

Alternatively you can use these two commands to check style manually:

.. sourcecode:: bash

    $ bin/pyflakes collective/table
    $ bin/pep8 collective/table


.. _changelog:

Changelog
=========

We track all feature-level changes to code inside ``docs/HISTORY.txt``. Examples:

- added feature X
- removed Y
- fixed bug Z
 

.. _sphinx-docs:

Sphinx documentation
====================

Un-documented code is broken code.

For every feature you add to the codebase you must also add documentation
for it in ``docs/sphinx/``.

After adding documentation, re-build `Sphinx` and check how it is displayed:

.. sourcecode:: bash

    $ bin/sphinxbuilder
    $ open docs/html/index.html


Sorting imports
===============

As a stylistic guide: Imports of code from other modules should always be 
alphabetically sorted with no empty lines between imports. The only exception
to this rule is to keep one empty line between a group of ``from x import y`` and 
a group of ``import y`` imports.

BAD

.. sourcecode:: python

    import os

    from plone.app.testing import login
    from collective.table.tests.base import TableIntegrationTestCase

GOOD

.. sourcecode:: python

    from collective.table.tests.base import TableIntegrationTestCase
    from plone.app.testing import login

    import os


Multiple imports
================

1. Don't use * to import `everything` from a module.
2. Don't use commas to import multiple stuff on a single line.
3. Don't use relative paths.

BAD

.. sourcecode:: python

    from collective.table.local import *
    from collective.table.local import add_row, delete_rows
    from .local import update_cell

GOOD

.. sourcecode:: python

    from collective.table.local import add_row
    from collective.table.local import delete_rows
    from collective.table.local import update_cell