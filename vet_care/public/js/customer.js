frappe.ui.form.on('Customer', {
    refresh: function(frm) {
        _set_dashboard(frm);
    }
});

function _set_dashboard(frm) {
    // Remove Subscriptions
    const filtered_sections = [__('Subscriptions')];
    const filtered_transactions = frm.dashboard.data.transactions.filter(function(transaction) {
        return !filtered_sections.includes(transaction.label);
    });
    frm.dashboard.data.transactions = filtered_transactions;

    // Remove Sales Order, Delivery Note under Orders
    const filtered_orders_items = ['Sales Order', 'Delivery Note'];
    const orders = filtered_transactions.find(function(transaction) {
        return transaction.label === __('Orders');
    });
    orders.items = orders.items.filter(function(item) {
        return !filtered_orders_items.includes(item);
    });

    // Add Patient on Orders
    orders.items.push('Patient');

    // Reload dashboard
    frm.dashboard.data_rendered = false;
    frm.dashboard.transactions_area.empty();
    frm.dashboard.refresh();
}