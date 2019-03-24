$(function() {
    let hoverClass = "table-info";

    // Highlight groups from type hovers
    $('tbody.item-listing > tr').hover(function() {
        let id = $(this).data('group-id');
        $('tbody.group-listing > tr[data-group-id='+id+']').addClass(hoverClass);
    }, function() {
        let id = $(this).data('group-id');
        $('tbody.group-listing > tr[data-group-id='+id+']').removeClass(hoverClass);
    });

    // Highlight types from group hovers
    $('tbody.group-listing > tr').hover(function() {
        let id = $(this).data('group-id');
        $('tbody.item-listing > tr[data-group-id='+id+']').addClass(hoverClass);
    }, function() {
        let id = $(this).data('group-id');
        $('tbody.item-listing > tr[data-group-id='+id+']').removeClass(hoverClass);
    });
});