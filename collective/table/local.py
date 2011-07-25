# -*- coding: utf-8 -*-
"""Simple, local ZODB storage of a table."""

from AccessControl import ClassSecurityInfo
from Products.Archetypes.utils import setSecurity
from collective.table import MessageFactory as _
from collective.table.interfaces import ILocalSource
from collective.table.source import BaseSource
from persistent.mapping import PersistentMapping
from zope import interface
from zope.annotation.interfaces import IAnnotations


class LocalSource(BaseSource):
    interface.implementsOnly(ILocalSource)
    security = ClassSecurityInfo()

    title = _(u'label_localsource', default=u'Locally stored')
    description = _(u'description_localsource',
        default=u'The rows for a local table are stored locally with the '
                u'content item')
    configurationView = '@@local-config'
    manageable = False

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

    security.declarePrivate('create_initial_row')
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

    security.declarePrivate('add_row')
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

    security.declarePrivate('delete_rows')
    def delete_rows(self, idxs):
        """Delete (multiple) row."""
        rows = self._annotations.get('rows')
        for index, row in enumerate(rows):
            if row['DT_RowId'] in idxs:
                del rows[index]
        self._annotations._p_changed = True

    security.declarePrivate('unset')
    def unset(self, name, instance, **kwargs):
        pass


setSecurity(LocalSource)
