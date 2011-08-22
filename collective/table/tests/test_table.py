# -*- coding: utf-8 -*-
"""Tests for Table content type."""

from collective.table.tests.base import TableIntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

import unittest2 as unittest


class TestTable(TableIntegrationTestCase):
    """Test an instance of Table content-type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_table_addable(self):
        """Tests if a Table can be added to the site."""

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Table', 'table',
                             title="Table Title",
                             description="Table Description",
                             text="<b>Table</b> Text",
                             )

        table = self.portal.table
        self.assertEquals(table.Title(), "Table Title")
        self.assertEquals(table.Description(), "Table Description")
        self.assertEquals(table.getText(),
                          "<p>&lt;b&gt;Table&lt;/b&gt; Text</p>")


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
