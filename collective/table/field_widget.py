# To manage expectations, the data table is managed as an archetypes field
from zope import component, interface, schema
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Widget import TypesWidget

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

    def getSource(self, instance):
        # XXX: setter and getters for the adapter name
        source = u'local'
        return component.getMultiAdapter(
            (self, instance), ISource, name=source)


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


