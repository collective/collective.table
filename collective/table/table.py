from zope import component, interface, schema
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from .config import PROJECTNAME
from .interfaces import ITable, ISource
from . import MessageFactory as _


TableSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField('sourceName',
        default=u'local',
        required=True,
        vocabulary_factory='available-table-storages',
        enforceVocabulary=True,
        languageIndependent=True,
        widget=atapi.SelectionWidget(
            label=_(u'label_source', default=u'Data Sounce'),
            description=_(u'help_source',
                default=u'The source for the data shown in the table.'),
            modes=('edit',),
            condition='python:'
                'len(object.getField("sourceName").Vocabulary(object)) > 1',
        ),
    ),
))


def availableTableStorages(context):
    """List all registed storage types"""
    adapters = component.getAdapters((context,), ISource)
    vocabulary = schema.vocabulary.SimpleVocabulary
    terms = []
    for name, source in adapters:
        terms.append(
            vocabulary.createTerm(name, name, source.title))
    terms.sort(key=lambda t: t.title)
    return vocabulary(terms)


class Table(base.ATCTContent):
    interface.implements(ITable)
    schema = TableSchema
    security = ClassSecurityInfo()

    security.declarePrivate('getSource')
    def getSource(self):
        sourcename = self.getSourceName()
        return component.getAdapter(self, ISource, sourcename)


base.registerATCT(Table, PROJECTNAME)
