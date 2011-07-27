if (typeof(collective) == 'undefined')
    collective = {};
collective.table = (function($) {

    var Table = function(table, url, columns, editable, sortable, queryable) {
        var self = this;
        var swf_url = portal_url + "/++resource++jquery.datatables/extras/TableTools/" +
                                   "media/swf/copy_cvs_xls.swf";

        self.table = table.dataTable({
            sDom: 'T<"clear">lfrtip', // where in DOM to inject TableTools controls
            oTableTools: {
                sSwfPath: swf_url,  // url to SWF files for TableTools controls
                aButtons: [ "copy", "csv", "xls", "print"]
            },
            
            // only display sorting and filtering features if data source supports it
            bSort: sortable,
            bFilter: queryable,
            
            bInfo: true,              // TODO
            bPaginate: true,          // TODO
            bProcessing: true,        // display of a 'processing' indicator
            bServerSide: true,        // make an XHR request to the server for each draw of the information on the page
            aoColumns: columns,       // give DataTables specific instructions for each individual column -> don't read from DOM
            sAjaxSource: url + 'json_data',    // url from which DataTables should load the remote data
            fnDrawCallback: function () {      // each time data is returned from the server, DataTables will build new DOM elements,
                                               // so these need the jEditable event handlers applied to them
                $('td', self.table.fnGetNodes()).editable(url + 'update_cell', {
                    event: 'dblclick',
                    submitdata: function ( value, settings ) {                      // what to submit besides cell value
                        var rowId = self.table.fnGetPosition(this)[0];
                        var columnId = self.table.fnGetPosition(this)[2];
                        var sColumnName = self.table.fnSettings().aoColumns[columnId].sName;
                        return {
                            row_id: rowId,                      // numerical id (int) of row
                            column_name: sColumnName           // string id (dict key) of column
                        };
                    },
                    height: "14px"      // height of the editing text-field
                });
                $(table, 'tbody').click(function(event) {
                    $(self.table.fnSettings().aoData).each(function (){
                        $(this.nTr).removeClass('row_selected');
                    });
                    $(event.target.parentNode).addClass('row_selected');
                });
            }
        });
    };

    $(function() {
        $('.collective_table_source_config').click(function() {
            var configView = $(this).closest('.collective_table_config').find(':radio:checked').data('configurationView');
        });
    });

    return {
        Table: Table
    };
})(jQuery);

/* Add a click handler for the delete row button */
function fnDeleteRowClickHandler( table, url )
{
    $('#delete-row').click( function() {
        var aIds = new Array();
        var aSelectedRows = fnGetSelected( table );

        // build a list of row indexes of rows to delete
        for ( var i=0 ; i<aSelectedRows.length ; i++ )
        {
            aIds.push(aSelectedRows[i].id);
        }

        // do a user-blocking ajax request to server to delete rows
        // in data storage
        $.ajax({
            url: url + 'delete_rows',
            async: false,
            type: 'POST',
            data: ({'rows:list' : aIds}),
            traditional: true        // don't store rows key as 'rows[]'
           });

        table.fnDraw(); // redraw the table
    });

}

/* Get the rows which are currently selected */
function fnGetSelected( table )
{
    var aReturn = new Array();
    var aTrs = table.fnGetNodes();

    for ( var i=0 ; i<aTrs.length ; i++ )
    {
        if ( $(aTrs[i]).hasClass('row_selected') )
        {
            aReturn.push( aTrs[i] );
        }
    }
    return aReturn;
}

