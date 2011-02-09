# Simple, local ZODB storage of a table
from zope import component, interface
from Products.Archetypes.interfaces import IBaseObject

from .interfaces import ILocalSource, ITableField
from . import MessageFactory as _


class LocalSource(object):
    component.adapts(ITableField, IBaseObject)
    interface.implements(ILocalSource)

    title = _(u'label_localsource', default=u'Locally stored')
    configurationView = '@@local-config'

    def __init__(self, field, instance):
        self.field = field
        self.instance = instance

    def listColumns(self):
        return (
            dict(id='one', title=u'Column 1'),
            dict(id='two', title=u'Column 2'),
        )
