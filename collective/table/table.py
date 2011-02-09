from Products.Archetypes import atapi
from Products.ATContentTypes.content import document

from .config import PROJECTNAME
from .field_widget import DataTableField, DataTableWidget
from . import MessageFactory as _


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
