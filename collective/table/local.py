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
        columns = self.listColumns()
        row = dict()
        row['DT_RowId'] = 0  # this is the first row
        for column in columns:
            row[column['id']] = 'click here to enter data'
        self._annotations['rows'] = [row, ]

    def add_row(self):
        """Add a new row."""
        # get columns and rows
        columns = self.listColumns()
        rows = self._annotations.get('rows')

        # prepare new row
        row = dict()
        row['DT_RowId'] = len(rows)  # add an incremental id to new row
        for column in columns:
            row[column['id']] = 'click here to enter data'

        # save new row
        rows.append(row)
        self._annotations._p_changed = True

    def delete_row(self, index):
        """Delete a row."""
        rows = self._annotations.get('rows')
        del rows[index]
        self._annotations._p_changed = True

    security.declarePrivate('unset')
    def unset(self, name, instance, **kwargs):
        pass

    security.declarePrivate('total_entries')
    def total_entries(self):
        return len(self._annotations.get('rows'))

setSecurity(LocalSource)
