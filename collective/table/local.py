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
        if not self._annotations.get('rows'):
            self.create_initial_row()
        return self._annotations.get('rows')

    security.declarePrivate('update_cell')
    def update_cell(self, row_id, column_name, value):
        rows = self._annotations.get('rows')
        rows[row_id][column_name] = value
        self._annotations._p_changed = True

    security.declarePrivate('set')
    def set(self, name, instance, value, **kwargs):
        pass

    def create_initial_row(self):
        """Fill first row of data with placeholder text. Format:
        dict(col00='foo', col01='bar')
        """
        print "creating initial row!"
        columns = self.listColumns()
        row = dict()
        for column in columns:
            row[column['id']] = 'click here to enter data'
        self._annotations['rows'] = (row, )

    security.declarePrivate('unset')
    def unset(self, name, instance, **kwargs):
        pass

    security.declarePrivate('total_entries')
    def total_entries(self):
        return len(self._annotations.get('rows'))

setSecurity(LocalSource)
