# Simple, local ZODB storage of a table
from zope import interface
from zope.annotation.interfaces import IAnnotations
from AccessControl import ClassSecurityInfo
from persistent.mapping import PersistentMapping
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

    @property
    def _annotations(self):
        mapping = IAnnotations(self.instance).setdefault(
            'collective.table.local', PersistentMapping())
        return mapping.setdefault(self.field.getName(), PersistentMapping())

    security.declarePrivate('listColumns')
    def listColumns(self):
        return self._annotations.get('columns', ())

    security.declarePrivate('setColumns')
    def setColumns(self, columns):
        self._annotations['columns'] = columns

    security.declarePrivate('get')
    def get(self, name, instance, **kwargs):
        return (
            ('Cell 1-1', 'Cell 1-2'),
            ('Cell 2-1', 'Cell 2-2'),
            ('Cell 3-1', 'Cell 3-2'),
        )

    security.declarePrivate('set')
    def set(self, name, instance, value, **kwargs):
        pass

    security.declarePrivate('unset')
    def unset(self, name, instance, **kwargs):
        pass

setSecurity(LocalSource)
