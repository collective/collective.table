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
        });
    };

    return {
        Table: Table
    };
})(jQuery);


function fnClickAddRow() {
    $('#table-table-datagrid').dataTable().fnAddData( [
        "1",
        "2"] );
}