from Products.ATContentTypes.content import document
from Products.Archetypes import atapi
from collective.table import MessageFactory as _
from collective.table.config import PROJECTNAME
from collective.table.field_widget import DataTableField
from collective.table.field_widget import DataTableWidget


TableSchema = document.ATDocumentSchema.copy() + atapi.Schema((
    DataTableField('table',
        languageIndependent=False,
        widget=DataTableWidget(
            label=_(u'label_table', u'Data table'),
            description=u'',
        ),
    ),
))

TableSchema.moveField('table', before='text')
TableSchema['presentation'].widget.condition = 'python:False'
TableSchema['tableContents'].widget.condition = 'python:False'


class Table(document.ATDocumentBase):
    schema = TableSchema


document.registerATCT(Table, PROJECTNAME)
