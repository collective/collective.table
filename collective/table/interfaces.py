# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.Archetypes.interfaces import IObjectField
from Products.Archetypes.interfaces import IStorage
from collective.table import MessageFactory as _
from zope import schema
from zope.interface import Interface


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
        title=_(u'Title'),
        description=_(u'Human-readable title of the data source'),
        required=True)

    description = schema.Text(
        title=_(u'Description'),
        description=_(u'Human-readable longer description of the data source'),
        required=True)

    configurationView = schema.ASCIILine(
        title=_(u'Configuration View'),
        description=_(u'The name of the view used to configure this source'),
        required=True)

    editable = schema.Bool(
        title=_(u'Supports editing'),
        description=_(u'True if this source supports editing existing '
                       'and adding new records.'),
        required=True)

    sortable = schema.Bool(
        title=_(u'Supports sorting'),
        description=_(u'True if this source supports sorting records by '
                       'clicking on columns.'),
        required=True)

    queryable = schema.Bool(
        title=_(u'Supports querying'),
        description=_(u'True if this source supports filtering records '
                       'by specifying a search query.'),
        required=True)

    def listColumns():
        """Return a sequence of dicts specifying the columns

        Each dict must have an id and a title column; ids must be ASCII, but
        titles are unicode strings.

        The columns will be displayed in the order they are listed.
        """


class ISourceConfiguration(Interface):
    """Base source configuration adapter interface.

    Concrete subclasses of this interface, are used to configure their
    ISource sources.
    """
    pass


class ILocalSource(ISource):
    """Local Source adapter interface."""
    pass


class ILocalSourceConfiguration(ISourceConfiguration):
    """Local Source configuration adapter interface."""
    columns = schema.List(
        title=_(u'Columns'),
        description=_(u'Specify the list of columns used in this table'),
        value_type=schema.TextLine(title=_(u'Column')),
        default=[u'Column 1', u'Column 2']
    )
