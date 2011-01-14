from zope import interface, schema


class ITable(interface.Interface):
    """A data table content type."""

    def getSource(self):
        """Return the currently selected data source"""


class ISource(interface.Interface):
    """Base source adapter interface.

    Concrete subclasses of this interface, registered as named adapters for
    ITable, are listed on the edit tab as source types to select from.

    """

    title = schema.TextLine(
        title=u'Title',
        description=u'Human-readable title of the data source',
        required=True)

    configurationView = schema.ASCIILine(
        title=u'Configuration View',
        description=u'The name of the view used to configure this source',
        required=True)

    def listColumns():
        """Return a sequence of dicts specifying the columns

        Each dict must have an id and a title column; ids must be ASCII, but
        titles are unicode strings.

        The columns will be displayed in the order they are listed.

        """


class ILocalSource(ISource):
    pass
