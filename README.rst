Easy storage of tabular data
============================


collective.table is a replacement for the "store equipment lists, book loans,
etc. in Excel files and upload to Plone". It's a list of items where members
can add/edit columns and rows and of course data. By default, collective.table
stores it's data in the ZODB, however storage is pluggable and it's easy to
write storage adapters to have data stored in SQL, LDAP, etc.

collective.table is based on `DataTables <http://datatables.net>`_ and
`jEditable <http://www.appelsiini.net/projects/jeditable>`_ jQuery plugins.

Developer documentation is available at `ReadTheDocs.org
<http://readthedocs.org/docs/collectivetable/en/latest/>`_.


Installation
============

To install collective.table you simply add ``collective.table`` to the list of
eggs in your buildout, run buildout and restart the Plone server. In Plone's
portal_quickinstaller you select ``collective.table`` and install it.

Now you can add a Table content-type and start adding your tabular data.


Usage
=====

Upon adding a new table you have to specify which columns you would like. You
do that by entering column names, one per line, into `columns` field. When you
click save your table will be created, containing one initial row. At the
moment, all columns are of type `string`.

Edit
----
Double-click on a cell of your choosing and enter something. Hitting `Enter`
will save this value.

Add a new row
-------------
Click the `Create a new row` button and a new row will be appended, which you
can  edit to enter your data.

Deleting a row
--------------
Start by selecting a row by clicking on it. Then click the `Delete this row`
button and this row will be deleted. You can select and delete multiple rows. 
