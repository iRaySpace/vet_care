frappe.ui.form.on('Patient', {
    vc_deceased: function(frm) {
        frappe.msgprint(
            'This animal information will be disabled. No further invoicing would be possible.',
            'Warning'
        );
    }
});
