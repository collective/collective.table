import json
from zope import component, interface
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse, NotFound
from zope.traversing.interfaces import ITraversable, TraversalError
from ZPublisher.BaseRequest import DefaultPublishTraverse

from ..interfaces import ISource


TABLEINIT = u"""\
(function($) { $(function() {
    new collective.table.Table(
        $('#%(fieldName)s-table-datagrid'), 
        '%(url)s', %(columns)s);
}); })(jQuery);
"""


class TableWidget(BrowserView):
    interface.implements(IPublishTraverse, ITraversable)

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
        adapters = component.getAdapters((self.field, self.context), ISource)
        current = self.field.sourceName
        sources = []
        for name, source in adapters:
            sources.append(dict(
                id=name, title=source.title, 
                description=source.description,
                selected=(name == current)
            ))
        return sources

    @property
    def source(self):
        return self.field.getSource(self.context)

    def tableinit(self):
        columndefs = []
        for column in self.source.listColumns():
            columndefs.append(dict(
                sName=column['id'],
                sTitle=column['title'],
            ))
        columns = json.dumps(columndefs)

        url = '%s/@@%s/%s/json_data' % (
            self.context.absolute_url(), self.__name__, self.fieldName)

        return TABLEINIT % dict(
            fieldName=self.fieldName, url=url, columns=columns
        )

    def json_data(self):
        """Return data from the source"""

        self.request.response.setHeader('content-type', 'application/json')

        return json.dumps(dict(
            aaData=(
                ('Cell 1-1', 'Cell 1-2'),
                ('Cell 2-1', 'Cell 2-2'),
            ),
        ))
