# -*- coding: utf-8 -*-
"""Tests for local storage."""

import mock
import unittest2 as unittest

from collective.table.tests.base import TableIntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles


class TestColumns(TableIntegrationTestCase):
    """Unit-tests for columns getter/setter methods of local.py."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Table', 'table')

    def makeLocalSource(self):
        """Prepare an instance of LocalSource"""
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


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
