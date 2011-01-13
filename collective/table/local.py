# Simple, local ZODB storage of a table
from zope import component, interface

from .interfaces import ILocalSource, ITable
from . import MessageFactory as _


class LocalSource(object):
    component.adapts(ITable)
    interface.implements(ILocalSource)

    title = _(u'label_localsource', default=u'Locally stored')
    configurationView = '@@local-config'

    def __init__(self, context):
        self.context = context
