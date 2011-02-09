if (typeof(collective) == 'undefined')
    collective = {};
collective.table = (function($) {
    var Table = function(table, url, columns) {
        var self = this;

        self.table = table.dataTable({
            aoColumns: columns,
            sAjaxSource: url
        })
    };

    return {
        Table: Table
    }
})(jQuery);
