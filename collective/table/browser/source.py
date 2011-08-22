# -*- coding: utf-8 -*-
"""Base Source configuration, serving as an example for other sources."""

from ZPublisher.BaseRequest import DefaultPublishTraverse
from collective.table import MessageFactory as _
from collective.table.interfaces import ISource
from plone.z3cform import layout
from z3c.form import form, button
from zope import component, interface, publisher, traversing


class BaseSourceConfigurationForm(form.Form):
    fieldName = None

    @property
    def prefix(self):
        return 'form.source.%s.%s.' % (self.sourceName, self.fieldName)

    @button.buttonAndHandler(_('Close'), name='close')
    def handleClose(self, action):
        # This action only exists to provide a button on the overlay-loaded
        # form. All source configuration handling is handled in a separate
        # API.
        pass

    def getContent(self):
        return self.getConfiguration()

    def applyChanges(self):
        data, errors = self.extractData()
        content = self.getContent()
        if errors:
            self.status = self.formErrorsMessage
            return

        changes = form.applyChanges(self, content, data)
        # ``changes`` is a dictionary; if empty, there were no changes
        if changes:
            self.setConfiguration(content)
        return changes

    @property
    def source(self):
        assert self.sourceName is not None, (
            _('Configuration form should set the sourceName attribute'))
        field = self.context.Schema()[self.fieldName]
        return component.getMultiAdapter(
            (field, self.context), ISource, name=self.sourceName)

    #
    # Sub-classes should provide the following methods and attributes
    #

    sourceName = None

    def getConfiguration(self):
        """Returns a dictionary with the configuration keyed on the form
        fields."""

        raise NotImplementedError()

    def setConfiguration(self, config):
        """Update the source configuration, given the config dict."""

        raise NotImplementedError()


class BaseSourceFormWrapper(layout.FormWrapper):
    interface.implements(publisher.interfaces.IPublishTraverse,
        traversing.interfaces.ITraversable)

    # ITraversable interface, for path traversing
    def traverse(self, name, further_path=[]):
        form = self.form_instance
        if form.fieldName is None and name in self.context.Schema():
            form.fieldName = name
            return self
        return getattr(self, name)

    # IPublishTraverse interface, for URL access
    def publishTraverse(self, request, name):
        try:
            return self.traverse(name)
        except traversing.interfaces.TraversalError:
            pass
        try:
            return super(BaseSourceFormWrapper, self).publishTraverse(request, name)
        except publisher.interfaces.NotFound:
            default = DefaultPublishTraverse(self, request)
            return default.publishTraverse(request, name)

    # Classical OFS.Traverse only supports bobo_traverse
    def __bobo_traverse__(self, request, name):
        return self.publishTraverse(request, name)


def wrap_form(form, **kwargs):
    return layout.wrap_form(form, BaseSourceFormWrapper, **kwargs)
