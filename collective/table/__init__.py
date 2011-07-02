from zope.i18nmessageid import MessageFactory
from . import config

MessageFactory = MessageFactory('collective.table')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    from Products.CMFCore.utils import ContentInit
    try:
        from Products.LinguaPlone import public as atapi
    except ImportError:
        from Products.Archetypes import atapi

    from .table import Table

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME), config.PROJECTNAME)
    for atype, constructor in zip(content_types, constructors):
        ContentInit('%s: %s' % (config.PROJECTNAME, atype.meta_type),
            content_types=(atype,),
            permission=config.ADD_PERMISSION,
            extra_constructors=(constructor,),
        ).initialize(context)
