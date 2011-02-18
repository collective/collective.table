if (typeof(collective) == 'undefined')
    collective = {};
collective.table = (function($) {
    TableToolsInit.sSwfPath = portal_url + 
        "/++resource++jquery.datatables/extras/TableTools/" +
        "media/swf/ZeroClipboard.swf";
    var Table = function(table, url, columns) {
        var self = this;

        self.table = table.dataTable({
            sDom: 'T<"clear">lfrtip',
            aoColumns: columns,
            sAjaxSource: url
        })
    };

    return {
        Table: Table
    };
})(jQuery);
