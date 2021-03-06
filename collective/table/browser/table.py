# -*- coding: utf-8 -*-
"""The TableWidget that displays and handles the DataTables table."""

from ZPublisher.BaseRequest import DefaultPublishTraverse
from collective.table.interfaces import ISource
from zope.component import getAdapters
from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError

import json

TABLEINIT = u"""\
(function($) { $(function() {
    var datatable = new collective.table.Table(
        $('#%(fieldName)s-table-datagrid'),
        '%(url)s', %(columns)s, %(editable)s, %(sortable)s, %(queryable)s);
}); })(jQuery);
"""


class TableWidget(BrowserView):
    implements(IPublishTraverse, ITraversable)

    fieldName = None

    # ITraversable interface, for path traversing
    def traverse(self, name, further_path=[]):
        if self.fieldName is None and name in self.context.Schema():
            self.fieldName = name
            return self
        return getattr(self, name)

    # IPublishTraverse interface, for URL access
    def publishTraverse(self, request, name):
        try:
            return self.traverse(name)
        except TraversalError:
            pass
        try:
            return super(TableWidget, self).publishTraverse(request, name)
        except NotFound:
            default = DefaultPublishTraverse(self, request)
            return default.publishTraverse(request, name)

    @property
    def macros(self):
        # The Archetypes widget machinery insists on .macros (attribute)
        return self['macros']

    @property
    def field(self):
        return self.context.Schema()[self.fieldName]

    def availableSources(self):
        adapters = getAdapters((self.field, self.context), ISource)
        current = self.field.getSourceName(self.context)
        sources = []
        configURL = '%s/%%s/%s' % (self.context.absolute_url(), self.fieldName)
        for name, source in adapters:
            sources.append(dict(
                id=name, title=source.title,
                description=source.description,
                configurationView=configURL % source.configurationView,
                selected=(name == current)
            ))
        return sources

    @property
    def source(self):
        return self.field.getSource(self.context)

    def url(self):
        return '%s/@@%s/%s/' % (self.context.absolute_url(),
                                self.__name__, self.fieldName)

    def tableinit(self):
        columndefs = []
        for column in self.source.listColumns():
            columndefs.append(dict(
                sTitle=column['title'],
                sName=column['id'],
                mDataProp=column['id'],
            ))
        columns = json.dumps(columndefs)

        return TABLEINIT % dict(
            fieldName=self.fieldName,
            url=self.url(),
            columns=columns,
            editable=self.source.editable and 'true' or 'false',
            sortable=self.source.sortable and 'true' or 'false',
            queryable=self.source.queryable and 'true' or 'false',
        )

    def json_data(self):
        """Return data from the source"""

        self.request.response.setHeader('content-type', 'application/json')
        start = int(self.request.get('iDisplayStart', 0))
        end = start + int(self.request.get('iDisplayLength', 10))
        data = self.field.get(self.context)
        result = json.dumps(dict(
            aaData=data[start:end],
            sEcho=self.get_sEcho(),
            iTotalRecords=len(data),
            iTotalDisplayRecords=len(data),
        ))
        return result

    def get_sEcho(self):
        """Table draw count sent from the client side. Convert it to integer
        to prevent XSS attacks."""
        return int(self.request['sEcho'])

    def update_cell(self):
        """Update a single cell in our dataset."""
        row_id = int(self.request['row_id'])
        column_name = self.request['column_name']
        value = self.request['value']
        self.source.update_cell(row_id, column_name, value)
        return value  # jEditable expects the sent value to be returned back

    def add_row(self):
        """Add a single row to our dataset."""
        self.source.add_row()
        self.request.response.redirect(self.context.absolute_url())

    def delete_rows(self):
        """Deletes (multiple) rows from our dataset."""
        rows = self.request.get('rows')
        if not rows:
            return None

        row_idxs = []
        for row_idx in rows:
            try:
                row_idx = int(row_idx)
                row_idxs.append(row_idx)
            except ValueError:
                print "Error casting row_idx to int: " + row_idx
        self.source.delete_rows(row_idxs)
