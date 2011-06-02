# -*- coding: utf-8 -*-
"""Tests for installation and setup of collective.table package."""

from Products.CMFCore.utils import getToolByName
from collective.table.tests.base import TableIntegrationTestCase

import unittest2 as unittest


class TestInstall(TableIntegrationTestCase):
    """Test installation of collective.table into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_product_installed(self):
        """Test if collective.table is installed with
        portal_quickinstaller.
        """
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('collective.table'))

    # types.xml
    # factorytool.xml
    def test_table_installed(self):
        """Test if Table is in the list of Portal Types."""

        # test that Table is added to portal_types
        types = getToolByName(self.portal, 'portal_types')
        self.failUnless('Table' in types.objectIds())

        # test that Table is added to portal_factory
        factory = getToolByName(self.portal, 'portal_factory')
        self.failUnless('Table' in factory.getFactoryTypes().keys())

    # rolemap.xml
    def test_permission_mappings(self):
        """Test correct assigning of permissions."""

        # Test permission mapping for adding an Table
        self.assertEquals(('Manager', 'Contributor', 'Owner'),
                          self.portal._collective_table__Add_Table_Permission)

    # jsregistry.xml
    def test_js_registered(self):
        """Test if JS files are registered with portal_javascripts."""
        resources = self.portal.portal_javascripts.getResources()

        ids = [r.getId() for r in resources]

        self.assertTrue('++resource++jquery.datatables/extras/TableTools/media/ZeroClipboard/ZeroClipboard.js' in ids,
                        'ZeroClipboard.js not found in portal_css')

        self.assertTrue('++resource++jquery.datatables/extras/TableTools/media/js/TableTools.min.js' in ids,
                        'ZeroClipboard.js not found in portal_css')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
