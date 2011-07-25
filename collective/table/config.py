# -*- coding: utf-8 -*-
"""Global constants and configuration."""

from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = 'collective.table'
GLOBALS = globals()

ADD_PERMISSION = 'collective.table: Add Table'
setDefaultRoles(ADD_PERMISSION, ('Owner', 'Manager'))
