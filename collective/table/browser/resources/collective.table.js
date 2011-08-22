if (typeof(collective) == 'undefined')
    collective = {};
collective.table = (function($) {

    //
    // Table view handling
    //
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

        table.closest('.dataTables_wrapper').prevAll('.datagrid-delete-row').click( function() {
            var selected = $(self.table.fnGetNodes()).filter('.row_selected'),
                aIds = $.map(selected, function(row) { return row.id; });

            // do a user-blocking ajax request to server to delete rows
            // in data storage
            $.ajax({
                url: url + 'delete_rows',
                async: false,
                type: 'POST',
                data: ({'rows:list' : aIds}),
                traditional: true        // don't store rows key as 'rows[]'
               });

            self.table.fnDraw(); // redraw the table
        });
    };


    //
    // Table configuration handling
    //
    $(function() {
        var configOpenLinks = $('a.collective_table_source_config');
        if (configOpenLinks.length) {
            // For each 'source configuration link', attach an overlay that'll
            // load the source config view, and attach a handler to the source
            // selection radios to set what view will be loaded. Handle data
            // from the form so we can save it together with the overall
            // Archetypes edit form POST.
            configOpenLinks.each(function() {
                var self = $(this),
                    tableConfig = self.closest('.collective_table_config'),
                    sourceConfig = tableConfig.find('div.collective_table_source_configuration');
                self.prepOverlay({
                    subtype: 'ajax',
                    formselector: '#content-core form',
                    beforepost: function(form, data) {
                        // Remember the form parameters for POST-ing
                        sourceConfig.empty();
                        $.each(data, function() {
                            sourceConfig.append(
                                $('<input type="hidden" name="' + this.name + '"/>')
                                    .val(this.value));
                        });
                        tableConfig.find(':radio:checked').data('currentConfig', $.param(data));
                        sourceChange();
                        form.closest('.overlay-ajax').overlay().close();
                        return false;
                    },
                    config: {
                        onBeforeLoad: function() {
                            // plone.app.z3cform includes form unloading protection
                            // by default, remove this protection again on load.
                            var tool = window.onbeforeunload && window.onbeforeunload.tool;
                            if (tool) {
                                tool.removeForms.apply(tool, this.getOverlay().get(0));
                            }
                            return true;
                        }
                    }
                });
                function sourceChange() {
                    var selected = tableConfig.find(':radio:checked'),
                        currentConfig = selected.data('currentConfig'),
                        configView = selected.data('configurationView'),
                        pbo = self.data('pbo');
                    if (currentConfig) configView = configView + '?' + currentConfig;

                    if (typeof(pbo) != 'undefined') {
                        // collective.js.jquerytools 1.2 and up
                        pbo.src = configView;
                    } else {
                        // collective.js.jquerytools < 1.2
                        $(self.attr('rel')).data('target') = configView;
                    }                    
                }
                tableConfig.find(':radio').change(sourceChange);
                sourceChange();
            });
        }
    });

    return {
        Table: Table
    };
})(jQuery);
