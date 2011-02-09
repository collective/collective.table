# Simple, local ZODB storage of a table
from zope import interface
from AccessControl import ClassSecurityInfo
from Products.Archetypes.utils import setSecurity

from .interfaces import ILocalSource
from .source import BaseSource
from . import MessageFactory as _


class LocalSource(BaseSource):
    interface.implementsOnly(ILocalSource)
    security = ClassSecurityInfo()

    title = _(u'label_localsource', default=u'Locally stored')
    description = _(u'description_localsource', 
        default=u'The rows for a local table are stored locally with the '
                u'content item')
    configurationView = '@@local-config'

    security.declarePrivate('listColumns')
    def listColumns(self):
        return (
            dict(id='one', title=u'Column 1'),
            dict(id='two', title=u'Column 2'),
        )

    security.declarePrivate('get')
    def get(self, name, instance, **kwargs):
        pass

    security.declarePrivate('set')
    def set(self, name, instance, value, **kwargs):
        pass

    security.declarePrivate('unset')
    def unset(self, name, instance, **kwargs):
        pass

setSecurity(LocalSource)
