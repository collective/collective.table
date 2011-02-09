from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from .config import PROJECTNAME
from .field_widget import DataTableField, DataTableWidget
from . import MessageFactory as _


TableSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    DataTableField('table',
        languageIndependent=False,
        widget=DataTableWidget(
            label=_(u'label_table', u'Data table'),
            description=u'',
        ),
    ),
))


class Table(base.ATCTContent):
    schema = TableSchema


base.registerATCT(Table, PROJECTNAME)
