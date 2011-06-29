if (typeof(collective) == 'undefined')
    collective = {};
collective.table = (function($) {

    var Table = function(table, url, columns) {
        var self = this;
        var swf_url = portal_url + "/++resource++jquery.datatables/extras/TableTools/" +
                                   "media/swf/copy_cvs_xls.swf";

        self.table = table.dataTable({
            sDom: 'T<"clear">lfrtip', // where in DOM to inject TableTools controls
            oTableTools: {
                sSwfPath: swf_url,  // url to SWF files for TableTools controls
                aButtons: [ "copy", "csv", "xls", "print"]
            },
            bProcessing: true,        // display of a 'processing' indicator
            bServerSide: true,        // make an XHR request to the server for each draw of the information on the page
            aoColumns: columns,       // give DataTables specific instructions for each individual column -> don't read from DOM
            sAjaxSource: url + 'json_data',    // url from which DataTables should load the remote data
            fnDrawCallback: function () {      // each time data is returned from the server, DataTables will build new DOM elements,
                                               // so these need the jEditable event handlers applied to them
                $('td', self.table.fnGetNodes()).editable(url + 'update_cell', {
                    submitdata: function ( value, settings ) {                      // what to submit besides cell value
                        var rowId = self.table.fnGetPosition(this)[0];
                        var columnId = self.table.fnGetPosition(this)[2];
                        var sColumnName = self.table.fnSettings().aoColumns[columnId].sName;
                        return {
                            row_id: rowId,                      // numerical id (int) of row
                            column_name: sColumnName,           // string id (dict key) of column
                        };
                    },
                    height: "14px"      // height of the editing text-field
                });
            }
        });
    };

    return {
        Table: Table
    };
})(jQuery);
