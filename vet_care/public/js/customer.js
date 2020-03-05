frappe.ui.form.on('Customer', {
    refresh: function(frm) {
        _add_patient_link(frm);
    }
});

function _add_patient_link(frm) {
    const pre_sales = frm.dashboard.data.transactions.find(({ label }) => label === __('Pre Sales'));
    if (pre_sales && !pre_sales.items.includes('Patient')) {
        pre_sales.items = ['Patient', ...pre_sales.items];
        frm.dashboard.data_rendered = false;
        frm.dashboard.transactions_area.empty();
        frm.dashboard.refresh();
    }
}
