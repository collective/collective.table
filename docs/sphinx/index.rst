============================================
Developer documentation for collective.table
============================================

:Project title: collective.table
:Latest version: 1.1
:Project page: http://pypi.python.org/pypi/collective.table
:Source: http://github.com/collective/collective.table

""""""""""""""""""""""""""""""""

.. topic:: Summary

    This is a Plone 4 add-on project for storing tabular data inside Plone,
    replacing the "store equipment lists, book loans, etc. in Excel files and
    upload to Plone". It's a list of items where members can add/edit columns
    and rows and of course data. By default, collective.table stores it's data
    in the ZODB, however storage is pluggable and it's easy to write storage
    adapters to have data stored in SQL, LDAP, etc. It is based on `DataTables
    <http://datatables.net>`_ and `jEditable
    <http://www.appelsiini.net/projects/jeditable>`_ jQuery plugins.

Table of Contents
=================

.. toctree::
   :maxdepth: 3

   glossary.rst
   dev.rst
   api.rst


Quick start
===========

If you have a Linux or OS X system already capable of running Plone then a
quick start with `collective.table` is as follows:

.. sourcecode:: bash

   $ git checkout git@github.com:collective/collective.table.git
   $ cd collective.table/
   $ virtualenv -p python2.6 --no-site-packages ./
   $ bin/python bootstrap.py
   $ bin/buildout
   $ bin/instance fg


.. include:: ../HISTORY.txt

.. include:: ../FUTURE.txt

.. include:: ../CREDITS.txt


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
