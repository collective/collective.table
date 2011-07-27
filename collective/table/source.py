# -*- coding: utf-8 -*-
"""Table data sources are masquerading as Archetypes Storages."""

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Storage import Storage
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.utils import setSecurity
from collective.table.interfaces import ITableField
from zope import component


class BaseSource(Storage):
    component.adapts(ITableField, IBaseObject)
    security = ClassSecurityInfo()

    title = None
    description = None
    configurationView = None
    editable = False
    sortable = False
    queryable = False

    def __init__(self, field, instance):
        self.field = field
        self.instance = instance

    security.declarePrivate('listColumns')
    def listColumns(self):
        raise NotImplementedError()

setSecurity(BaseSource)
