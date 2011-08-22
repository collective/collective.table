# -*- coding: utf-8 -*-
"""To manage expectations, the data table is managed as an archetypes field."""

from AccessControl import ClassSecurityInfo
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.exceptions import ObjectFieldException
from collective.table import MessageFactory as _
from collective.table.interfaces import ISource
from collective.table.interfaces import ITableField
from persistent.mapping import PersistentMapping
from zope import component
from zope import interface
from zope.annotation.interfaces import IAnnotations


class DataTableWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update(dict(
        macro='@@collective.table.widgets',
        helper_js=('++resource++collective.table/collective.table.js',),
        helper_css=('++resource++collective.table/collective.table.css',),
    ))
    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, **kw):
        sourceName = form.get('%s.sourceName' % field.getName())
        if not sourceName:
            raise Exception('we need to set the source')
        field.setSourceName(instance, sourceName)

        configView = field.getSource(instance).configurationView
        config = instance.unrestrictedTraverse(
            '%s/%s' % (configView, field.getName()))
        config.form_instance.update()

        # Extract your own form fields from the request
        changes = config.form_instance.applyChanges()
        # XXX: Handle changes = None and config.formErrorsMessage being set == ERROR

        return TypesWidget.process_form(self, instance, field, form, **kw)


class DataTableField(ObjectField):
    interface.implements(ITableField)
    widget = DataTableWidget
    security = ClassSecurityInfo()

    _properties = ObjectField._properties.copy()
    _properties.update({
        'defaultSourceName': 'local',
    })

    security.declarePrivate('setSourceName')
    def setSourceName(self, instance, value):
        """Set the name of the data source you want to use in this context."""
        mapping = IAnnotations(instance).setdefault(
            'collective.table',
            PersistentMapping()
        )
        mapping['source_name'] = value

    security.declarePrivate('getSourceName')
    def getSourceName(self, instance):
        """Get the name of the data source that is used in this context."""
        mapping = IAnnotations(instance).setdefault(
            'collective.table',
            PersistentMapping()
        )
        return mapping.get('source_name', self.defaultSourceName)

    security.declarePrivate('getSource')
    def getSource(self, instance):
        return component.getMultiAdapter(
            (self, instance), ISource, name=self.getSourceName(instance))

    # We are not a field in the usual manner, so we need to override some
    # things to clean things up
    security.declarePrivate('setStorage')
    def setStorage(self, instance, storage):
        raise ObjectFieldException("Not supported, \
            use field.setSourceName instead")

    security.declarePrivate('getStorage')
    def getStorage(self, instance=None):
        return self.getSource(instance)


registerWidget(DataTableWidget,
    title=_('Data Table'),
    description=_('Renders the complex data table and manage it\'s '
                'configuration'),
    used_for=('collective.table.field_widget.DataTableField',)
)
registerField(DataTableField,
    title=_('Data Table'), description=_('Complex data table with flexible sources'))
