# To manage expectations, the data table is managed as an archetypes field
from zope import component, interface
from AccessControl import ClassSecurityInfo
from Products.Archetypes.exceptions import ObjectFieldException
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerField, registerWidget

from .interfaces import ISource, ITableField


class DataTableWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update(dict(
        macro='@@collective.table.widgets',
        helper_js=('++resource++collective.table/collective.table.js',),
        helper_css=('++resource++collective.table/collective.table.css',),
    ))
    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, **kw):
        sourceName = form.get('%s.sourceName' % field.getName())
        if sourceName is not None:
            field.sourceName = sourceName

        # This should be handled at the source level, but until we have more
        # than one, it'll do here.
        columndefs = form.get('%s.local.columns' % field.getName())
        if columndefs is not None:
            columns = []
            counter = 0
            for line in columndefs.splitlines():
                title = line.strip()
                if not title:
                    continue
                columns.append(dict(id='col%02d' % counter, title=title))
                counter += 1
            field.getSource(instance).setColumns(columns)
        return TypesWidget.process_form(self, instance, field, form, **kw)


class DataTableField(ObjectField):
    interface.implements(ITableField)
    widget = DataTableWidget
    security = ClassSecurityInfo()

    _properties = ObjectField._properties.copy()
    _properties.update({
        'sourceName' : 'local',
    })

    security.declarePrivate('getSource')
    def getSource(self, instance):
        return component.getMultiAdapter(
            (self, instance), ISource, name=self.sourceName)

    # We are not a field in the usual manner, so we need to override some
    # things to clean things up
    security.declarePrivate('setStorage')
    def setStorage(self, instance, storage):
        raise ObjectFieldException, "Not supported, use field.setSource(name) instead"

    security.declarePrivate('getStorage')
    def getStorage(self, instance=None):
        return self.getSource(instance)


registerWidget(DataTableWidget,
    title='Data Table',
    description='Renders the complex data table and manage it\'s '
                'configuration',
    used_for=('collective.table.field_widget.DataTableField',)
)
registerField(DataTableField, 
    title='Data Table', description='Complex data table with flexible sources')
