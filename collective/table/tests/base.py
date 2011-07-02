# -*- coding: utf-8 -*-
"""Layers and TestCases for our tests."""

from __future__ import with_statement

import unittest2 as unittest

from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing.selenium_layers import SELENIUM_PLONE_FUNCTIONAL_TESTING


class TableLayer(PloneSandboxLayer):
    """Layer for collective.table tests."""

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.table
        self.loadZCML(package=collective.table)
        z2.installProduct(app, 'collective.table')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.table:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'collective.table')


# FIXTURES
TABLE_FIXTURE = TableLayer()

# LAYERS
INTEGRATION_TESTING = IntegrationTesting(
    bases=(TABLE_FIXTURE, ),
    name="collective.table:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TABLE_FIXTURE,),
    name="collective.table:Functional")


# TESTCASES
class TableIntegrationTestCase(unittest.TestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    layer = INTEGRATION_TESTING


class TableFunctionalTestCase(unittest.TestCase):
    """We use this base class for all functional tests in this package -
    tests that require a full-blown Plone instance for testing.
    """
    layer = FUNCTIONAL_TESTING


class TableSeleniumTestCase(TableFunctionalTestCase):
    """We use this base class for all functional tests in this package -
    tests that require a full-blown Plone instance for testing.
    """
    layer = SELENIUM_PLONE_FUNCTIONAL_TESTING
