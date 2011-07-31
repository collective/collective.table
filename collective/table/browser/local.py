from source import BaseSourceConfigurationForm, wrap_form
from z3c.form import field
from zope import interface, schema

from collective.table import MessageFactory as _


class ILocalSourceConfiguration(interface.Interface):
    columns = schema.List(
        title=_(u'Columns'),
        value_type=schema.TextLine(title=_(u'Column')),
        default=[u'Column 1', u'Column 2']
    )

class LocalSourceConfigurationForm(BaseSourceConfigurationForm):
    fields = field.Fields(ILocalSourceConfiguration)
    label = _(u'localsource-configuration', u'Configure local source')
    sourceName = 'local'

    def getConfiguration(self):
        source = self.source
        return dict(columns=[c['title'] for c in source.listColumns()])

    def setConfiguration(self, config):
        columns = []
        for i, title in enumerate(config.get('columns', [])):
            columns.append(dict(id='col%02d' % i, title=title))
        self.source.setColumns(columns)


LocalSourceConfigurationView = wrap_form(LocalSourceConfigurationForm)
