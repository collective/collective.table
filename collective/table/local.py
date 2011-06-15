# Simple, local ZODB storage of a table
from zope import interface
from zope.annotation.interfaces import IAnnotations
from AccessControl import ClassSecurityInfo
from persistent.mapping import PersistentMapping
from Products.Archetypes.utils import setSecurity

from .interfaces import ILocalSource
from .source import BaseSource
from . import MessageFactory as _


DEVELOPMENT_DEFAULT = (
    dict(col00='Cell 1-1', col01='Cell 1-2'),
    dict(col00='Cell 2-1', col01='Cell 2-2'),
    dict(col00='Cell 3-1', col01='Cell 3-2'),
)


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
        return self._annotations.get('rows', DEVELOPMENT_DEFAULT)

    security.declarePrivate('setColumns')
    def update_cell(self, row_id, column_name, value):
        DEVELOPMENT_DEFAULT[row_id][column_name] = value

    security.declarePrivate('set')
    def set(self, name, instance, value, **kwargs):
        pass

    security.declarePrivate('unset')
    def unset(self, name, instance, **kwargs):
        pass

setSecurity(LocalSource)
