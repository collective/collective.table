if (typeof(collective) == 'undefined')
    collective = {};
collective.table = (function($) {

    var Table = function(table, url, columns) {
        var self = this;
        var swf_url = portal_url + "/++resource++jquery.datatables/extras/TableTools/" +
                                   "media/swf/copy_cvs_xls.swf";

        self.table = table.dataTable({
            sDom: 'T<"clear">lfrtip',
            oTableTools: { sSwfPath: swf_url },
            aoColumns: columns,
            sAjaxSource: url
        })
    };

    return {
        Table: Table
    };
})(jQuery);
