if (typeof(collective) == 'undefined')
    collective = {};
collective.table = (function($) {
    // page init
    $(function() {
        $('#table-datagrid').dataTable();
    });
    return {};
})(jQuery);
