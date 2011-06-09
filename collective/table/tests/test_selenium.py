# -*- coding: utf-8 -*-
"""Tests for installation and setup of collective.table package."""

from Products.CMFCore.utils import getToolByName
from collective.table.tests.base import TableSeleniumTestCase
from plone.app.testing.selenium_layers import open, click, type

import unittest2 as unittest


class TestSelenium(TableSeleniumTestCase):
    """Test installation of collective.table into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']

    def test_product_installed(self):
        """Test if collective.table is installed with
        portal_quickinstaller.
        """
        open(self.driver, self.portal.absolute_url())
        self.assertTrue("Plone" in self.driver.get_page_source())
