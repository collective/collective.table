# -*- coding: utf-8 -*-
"""Tests for installation and setup of collective.table package."""

from collective.table.tests.base import TableSeleniumTestCase
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing.selenium_layers import click
from plone.app.testing.selenium_layers import open
from plone.app.testing.selenium_layers import type

import time


class TestSelenium(TableSeleniumTestCase):
    """Test installation of collective.table into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.driver = self.layer['selenium']
        self.portal = self.layer['portal']

    def login(self):
        """Login to the portal as Manager."""
        open(self.driver, self.portal.absolute_url() + '/login_form')

        # login as user
        type(self.driver, "__ac_name", TEST_USER_NAME)
        type(self.driver, "__ac_password", TEST_USER_PASSWORD)
        click(self.driver, "submit")
        time.sleep(5)
        self.driver.find_element_by_id("personaltools-logout")

        # assign role to user
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_add_table(self):
        """Test if Table can be added."""
        self.login()
        open(self.driver, self.portal.absolute_url())
        import pdb; pdb.set_trace( )
