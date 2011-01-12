from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from .config import PROJECTNAME

TableSchema = schemata.ATContentTypeSchema.copy()

class Table(base.ATCTContent):
    schema = TableSchema

base.registerATCT(Table, PROJECTNAME)
