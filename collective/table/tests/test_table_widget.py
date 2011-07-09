# -*- coding: utf-8 -*-
"""Tests for the table widget."""

import mock
import unittest2 as unittest

from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

from collective.table.tests.base import TableIntegrationTestCase


class TestTableWidgetIntegration(TableIntegrationTestCase):
    """Integration tests for the table widget."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Table', 'table')

    def makeTableWidget(self):
        """Prepare an instance of table widget."""
        from collective.table.browser.table import TableWidget
        context = self.portal.table
        widget = TableWidget(context, None)
        widget.fieldName = 'table'
        return widget

    def makeAdapter(self, name):
        """Prepare a mocked instance of an adapter."""
        adapter = mock.Mock(spec="title description".split())
        adapter.title = '%s title' % name
        adapter.description = '%s description' % name
        return adapter

    @mock.patch('collective.table.browser.table.getAdapters')
    @mock.patch('collective.table.browser.table.TableWidget.field')
    def test_available_sources(self, field, getAdapters):
        """Test retrieving available table sources."""

        # create some dummy adapters
        foo = self.makeAdapter('foo')
        bar = self.makeAdapter('bar')

        # make zope.interface.getAdapters return our dummy adapters
        getAdapters.return_value = [('foo', foo), ('bar', bar)]

        # mock field() property to return current source id
        field.sourceName.return_value = 'foo'

        # make widget and set foo as current source
        widget = self.makeTableWidget()

        # get available sources
        sources = widget.availableSources()

        # test output
        self.assertEquals(2, len(sources))

        self.assertEquals('foo', sources[0]['id'])
        self.assertEquals('foo title', sources[0]['title'])
        self.assertEquals('foo description', sources[0]['description'])
        self.assertEquals(True, sources[0]['selected'])

        self.assertEquals('bar', sources[1]['id'])
        self.assertEquals('bar title', sources[1]['title'])
        self.assertEquals('bar description', sources[1]['description'])
        self.assertEquals(False, sources[1]['selected'])


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
