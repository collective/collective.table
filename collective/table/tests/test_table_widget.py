# -*- coding: utf-8 -*-
"""Tests for the table widget."""

from collective.table.tests.base import TableIntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from zope.publisher.browser import TestRequest

import json
import mock
import unittest2 as unittest


class TestTableWidgetIntegration(TableIntegrationTestCase):
    """Integration tests for the table widget."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Table', 'table')

    def makeTableWidget(self):
        """Prepare an instance of table widget."""
        from collective.table.browser.table import TableWidget
        context = self.portal.table
        widget = TableWidget(context, None)
        widget.fieldName = 'table'
        return widget

    def makeSource(self, name):
        """Prepare a dummy instance of a ZCA adapter."""
        source = mock.Mock(spec="title description".split())
        source.title = '%s title' % name
        source.description = '%s description' % name
        source.configurationView = '@%s_configuration' % name
        return source

    def makeColumn(self, id, title):
        """Prepare a dummy instance of a table column."""
        return dict(id=id, title=title)

    @mock.patch('collective.table.browser.table.getAdapters')
    @mock.patch('collective.table.browser.table.TableWidget.field')
    def test_available_sources(self, field, getAdapters):
        """Test retrieving available table sources."""

        # create some dummy adapters
        foo = self.makeSource('foo')
        bar = self.makeSource('bar')

        # make zope.interface.getAdapters return our dummy adapters
        getAdapters.return_value = [('foo', foo), ('bar', bar)]

        # mock field() to return current source id
        field.getSourceName.return_value = 'foo'

        # make widget and set foo as current source
        widget = self.makeTableWidget()

        # get available sources
        sources = widget.availableSources()

        # test output
        self.assertEquals(2, len(sources))

        self.assertEquals('foo', sources[0]['id'])
        self.assertEquals('foo title', sources[0]['title'])
        self.assertEquals('foo description', sources[0]['description'])
        self.assertEquals(True, sources[0]['selected'])

        self.assertEquals('bar', sources[1]['id'])
        self.assertEquals('bar title', sources[1]['title'])
        self.assertEquals('bar description', sources[1]['description'])
        self.assertEquals(False, sources[1]['selected'])

    def test_url(self):
        """Test how url is constructed."""
        widget = self.makeTableWidget()
        widget.__name__ = 'table'
        self.assertEquals('http://nohost/plone/table/@@table/table/',
                          widget.url())

    @mock.patch('collective.table.browser.table.TableWidget.url')
    @mock.patch('collective.table.browser.table.TableWidget.source')
    def test_tableinit(self, source, url):
        """Test the Javascript that is injected inline and initializes
        our table."""

        # mock source.listColumns() to return some dummy columns
        source.listColumns.return_value = [
            self.makeColumn('foo', 'Foo'),
            self.makeColumn('bar', 'Bar')
            ]

        # mock source() properties to return True
        source.editable = True
        source.sortable = True
        source.queryable = True

        # mock url() property to return some url -> not really important which
        url.return_value = 'http://foo'

        # get the tableinit result dict
        widget = self.makeTableWidget()
        result = widget.tableinit()
        self.maxDiff = None
        # test the bleeep out of it
        expected = u"""\
(function($) { $(function() {
    var datatable = new collective.table.Table(
        $('#table-table-datagrid'),
        'http://foo', [{"sTitle": "Foo", "sName": "foo", "mDataProp": "foo"}, {"sTitle": "Bar", "sName": "bar", "mDataProp": "bar"}], true, true, true);
    var table = datatable.table
    fnDeleteRowClickHandler(table, 'http://foo')

}); })(jQuery);
"""
        self.assertEquals(expected, result)

    @mock.patch('collective.table.browser.table.TableWidget.field')
    def test_json_data(self, field):
        """Test how data from source is sent to our datatables table."""

        rows = [
            dict(DT_RowId=0, col00='foo1', col01='bar1'),
            dict(DT_RowId=1, col00='foo2', col01='bar2'),
            ]

        # mock field.get to return some dummy rows
        field.get.return_value = rows

        # instantiate widget
        widget = self.makeTableWidget()

        # use a real request object
        widget.request = TestRequest(sEcho=1)

        # get json data
        result = widget.json_data()
        result = json.loads(result)

        # test
        self.assertEquals(1, result['sEcho'])
        self.assertEquals(rows, result['aaData'])

    def test_get_sEcho(self):
        """Test sEcho request parameter -> table draw count that is used to
        prevent XSS attacks."""
        widget = self.makeTableWidget()
        widget.request = TestRequest(sEcho=1)
        self.assertEquals(1, widget.get_sEcho())

    @mock.patch('collective.table.browser.table.TableWidget.source')
    def test_add_row(self, source):
        """Test adding a new row."""
        widget = self.makeTableWidget()
        widget.request = mock.Mock()
        widget.add_row()

        # test that add_row in data source was called
        source.add_row.assert_called_once_with()

        # test that user is redirected back to table
        widget.request.response.redirect.assert_called_once_with('http://nohost/plone/table')

    @mock.patch('collective.table.browser.table.TableWidget.source')
    def test_delete_rows(self, source):
        """Test deleting a row."""
        widget = self.makeTableWidget()
        widget.request = TestRequest(rows=[1, 3, 5])
        widget.delete_rows()

        source.delete_rows.assert_called_once_with([1, 3, 5])

    @mock.patch('collective.table.browser.table.TableWidget.source')
    def test_update_cell(self, source):
        """Test updating a cell."""

        # fill test request with values
        form = dict(
            row_id=1,
            column_name='col01',
            value='foo'
            )

        widget = self.makeTableWidget()
        widget.request = TestRequest(form=form)
        result = widget.update_cell()

        self.assertEquals('foo', result)
        source.update_cell.assert_called_once_with(1, 'col01', 'foo')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
