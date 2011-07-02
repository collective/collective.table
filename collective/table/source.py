# Table data sources are masquerading as Archetypes Storages.
from zope import component
from AccessControl import ClassSecurityInfo
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.Storage import Storage
from Products.Archetypes.utils import setSecurity

from .interfaces import ITableField


class BaseSource(Storage):
    component.adapts(ITableField, IBaseObject)
    security = ClassSecurityInfo()

    title = None
    description = None
    configurationView = None
    sortable = False

    def __init__(self, field, instance):
        self.field = field
        self.instance = instance

    security.declarePrivate('listColumns')
    def listColumns(self):
        raise NotImplementedError()

setSecurity(BaseSource)
