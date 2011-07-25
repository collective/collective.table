# -*- coding: utf-8 -*-
"""Tests for local storage."""

from collective.table.tests.base import TableIntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

import mock
import unittest2 as unittest


class TestLocalSourceIntegration(TableIntegrationTestCase):
    """Integration tests for methods of local.py."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Table', 'table')

    def makeLocalSource(self):
        """Prepare an instance of LocalSource."""
        from collective.table.local import LocalSource
        field = mock.Mock(spec="getName".split())
        field.getName.return_value = 'table'
        context = self.portal.table
        return LocalSource(field, context)

    def test_list_no_columns(self):
        """Test return value when there is no 'columns' mapping
        in annotations."""
        local = self.makeLocalSource()
        self.assertEquals((), local.listColumns())

    def test_list_empty_columns(self):
        """Test return value when 'columns' mapping is empty."""
        local = self.makeLocalSource()
        local._annotations['columns'] = ()
        self.assertEquals((), local.listColumns())

    def test_list_some_columns(self):
        """Test return value when there are some columns in
        'columns' mapping."""
        local = self.makeLocalSource()
        local._annotations['columns'] = ('foo', 'bar')
        self.assertEquals(('foo', 'bar'), local.listColumns())

    def test_set_columns(self):
        """Test that 'columns' key is set."""
        local = self.makeLocalSource()
        local.setColumns(('foo', 'bar'))
        self.assertEquals(('foo', 'bar'), local._annotations['columns'])

    def test_get(self):
        """Test that get returns rows from _annotations."""
        local = self.makeLocalSource()
        local._annotations['rows'] = ['foo', 'bar']
        result = local.get('Table', self.portal.table)
        self.assertEquals(['foo', 'bar'], result)

    @mock.patch('collective.table.local.LocalSource.create_initial_row')
    def test_get_when_no_rows(self, create_initial_row):
        """Test that get calls create_initial_row if there are now rows."""
        local = self.makeLocalSource()
        local.get('Table', self.portal.table)
        create_initial_row.assert_called_once_with()

    @mock.patch('collective.table.local.LocalSource.listColumns')
    def test_create_initial_row(self, listColumns):
        """Test how initial row is created."""
        # make listColums() return some dummy columns
        listColumns.return_value = (dict(id='foo'), dict(id='bar'))

        local = self.makeLocalSource()
        local.create_initial_row()
        self.assertEquals(local._annotations['rows'],
                          [{'DT_RowId': 0,
                            'foo': 'click here to enter data',
                            'bar': 'click here to enter data'}])

    @mock.patch('collective.table.local.LocalSource.listColumns')
    def test_add_row(self, listColumns):
        """Test adding a new row."""
        # make listColums() return some dummy columns
        listColumns.return_value = (dict(id='foo'), dict(id='bar'))

        local = self.makeLocalSource()
        local.create_initial_row()  # this is needed because we do len(rows)
        local.add_row()
        row = local._annotations['rows'][0]
        self.assertEquals(row['foo'], 'click here to enter data')
        self.assertEquals(row['bar'], 'click here to enter data')

    def test_delete_rows(self):
        """Test deleting a row."""
        local = self.makeLocalSource()
        local._annotations['rows'] = [
            dict(id='foo', DT_RowId=1),
            dict(id='bar', DT_RowId=2),
            ]
        rows = local._annotations['rows']

        self.assertEquals(len(rows), 2)

        local.delete_rows([1])
        self.assertEquals(len(rows), 1)
        self.assertEquals(rows, [dict(id='bar', DT_RowId=2)])

    def test_update_cell(self):
        """Test that a cell gets updated."""
        local = self.makeLocalSource()
        local._annotations['columns'] = (dict(id='foo'))
        local._annotations['rows'] = [dict(foo='bar')]

        local.update_cell(0, 'foo', 'new value')
        self.assertEquals(local._annotations['rows'], [dict(foo='new value')])


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
