if (typeof(collective) == 'undefined')
    collective = {};
collective.table = (function($) {
    var Table = function(url, columns) {
        var self = this;

        self.table = $('table#table-datagrid').dataTable({
            aoColumns: columns,
            sAjaxSource: url
        })
    };

    return {
        Table: Table
    }
})(jQuery);
