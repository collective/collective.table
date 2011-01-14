import json
from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


TABLEINIT = u"""\
(function($) { $(function() {
    new collective.table.Table('%(url)s', %(columns)s);
}); })(jQuery);
"""


class TableView(BrowserView):
    template = ViewPageTemplateFile('templates/table.pt')
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.source = context.getSource()

    def __call__(self):
        return self.template()

    def tableinit(self):
        columndefs = []
        for column in self.source.listColumns():
            columndefs.append(dict(
                sName=column['id'],
                sTitle=column['title'],
            ))
        columns = json.dumps(columndefs)

        url = '%s/@@%s/json_data' % (
            self.context.absolute_url(), self.__name__)

        return TABLEINIT % dict(url=url, columns=columns)

    def json_data(self):
        """Return data from the source"""

        self.request.response.setHeader('content-type', 'application/json')

        return json.dumps(dict(
            aaData=(
                ('Cell 1-1', 'Cell 1-2'),
                ('Cell 2-1', 'Cell 2-2'),
            ),
        ))
