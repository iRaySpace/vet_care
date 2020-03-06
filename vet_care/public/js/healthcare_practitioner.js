frappe.ui.form.on('Healthcare Practitioner', {
    vc_out_of_clinic: function(frm) {
        if (frm.doc.vc_out_of_clinic) {
            frappe.msgprint('Any further bookings will not be available if Physician is out-of-clinic.', 'Out-of-clinic');
        }
    }
});
