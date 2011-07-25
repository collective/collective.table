.. collective.table documentation master file, created by
   sphinx-quickstart on Tue June 14 19:10:04 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to collective.table's documentation!
================================================================

:Project title: collective.table
:Latest version: |release|
:URL: http://pypi.python.org/pypi/collective.table

""""""""""""""""""""""""""""""""

.. topic:: Summary

    This is a Plone 4 add-on project for storing tabular data inside Plone.

Table of Contents
=================

.. toctree::
   :maxdepth: 3

   glossary.rst
   dev.rst
   api.rst


Quick start
===========

If you have a Linux or OS X system already capable of running Plone then a quick start with collective.table is as follows:

.. sourcecode:: bash

   $ git co git@github.com:nzupan/collective.table.git
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
