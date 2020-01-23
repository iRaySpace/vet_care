frappe.ui.form.on('Patient', {
    onload: function(frm) {
        frm.set_query('customer', 'vc_pet_relation', function() {
            return { query: "erpnext.controllers.queries.customer_query" };
        });
    },
    vc_deceased: function(frm) {
        frappe.msgprint(
            'This animal information will be disabled. No further invoicing would be possible.',
            'Warning'
        );
    }
});
