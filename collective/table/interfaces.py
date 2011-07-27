# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""


from Products.Archetypes.interfaces import IObjectField
from Products.Archetypes.interfaces import IStorage
from zope import schema


class ITableField(IObjectField):
    """A data table field."""

    def getSource(self, instance):
        """Return the currently selected data source"""


class ISource(IStorage):
    """Base source adapter interface.

    Concrete subclasses of this interface, registered as named adapters for
    ITable, are listed on the edit tab as source types to select from.

    """

    title = schema.TextLine(
        title=u'Title',
        description=u'Human-readable title of the data source',
        required=True)

    description = schema.Text(
        title=u'Description',
        description=u'Human-readable longer description of the data source',
        required=True)

    configurationView = schema.ASCIILine(
        title=u'Configuration View',
        description=u'The name of the view used to configure this source',
        required=True)

    editable = schema.Bool(
        title=u'Supports editing',
        description=u'True if this source supports editing existing \
                      and adding new records.',
        required=True)

    sortable = schema.Bool(
        title=u'Supports sorting',
        description=u'True if this source supports sorting records by \
                      clicking on columns.',
        required=True)

    queryable = schema.Bool(
        title=u'Supports querying',
        description=u'True if this source supports filtering records \
                      by specifying a search query.',
        required=True)


    def listColumns():
        """Return a sequence of dicts specifying the columns

        Each dict must have an id and a title column; ids must be ASCII, but
        titles are unicode strings.

        The columns will be displayed in the order they are listed.

        """


class ILocalSource(ISource):
    pass
