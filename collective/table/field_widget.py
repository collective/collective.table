# To manage expectations, the data table is managed as an archetypes field
from zope import component, interface, schema
from AccessControl import ClassSecurityInfo
from Products.Archetypes.exceptions import ObjectFieldException
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerField

from .interfaces import ISource, ITableField


class DataTableWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update(dict(
        macro='@@collective.table.widgets',
        helper_js=('++resource++collective.table/collective.table.js',),
        helper_css=('++resource++collective.table/collective.table.css',),
    ))


class DataTableField(ObjectField):
    interface.implements(ITableField)
    widget = DataTableWidget
    security = ClassSecurityInfo()

    security.declarePrivate('getSource')
    def getSource(self, instance):
        # XXX: setter and getters for the adapter name
        source = u'local'
        return component.getMultiAdapter(
            (self, instance), ISource, name=source)

    # We are not a field in the usual manner, so we need to override some
    # things to clean things up
    security.declarePrivate('setStorage')
    def setStorage(self, instance, storage):
        raise ObjectFieldException, "Not supported, use field.setSource(name) instead"

    security.declarePrivate('getStorage')
    def getStorage(self, instance=None):
        return self.getSource(instance)


registerField(DataTableField, 
    title='Data Table', description='Complex data table with flexible sources')


def availableTableStorages(context):
    """List all registed storage types"""
    adapters = component.getAdapters((DataTableField(), context), ISource)
    vocabulary = schema.vocabulary.SimpleVocabulary
    terms = []
    for name, source in adapters:
        terms.append(
            vocabulary.createTerm(name, name, source.title))
    terms.sort(key=lambda t: t.title)
    return vocabulary(terms)


