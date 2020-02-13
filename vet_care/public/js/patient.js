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
    },
    vc_inpatient: async function(frm) {
        if (frm.doc.vc_inpatient) {
            const values = await vet_care.utils.prompt_admission_dialog();
            frm.doc.__new_patient_activity = true;
            frm.doc.__reason = values.reason;
            frm.doc.__posting_date = values.posting_date;
            frm.doc.__posting_time = values.posting_time;
        } else {
            const values = await vet_care.utils.prompt_discharge_dialog();
            frm.doc.__new_patient_activity = true;
            frm.doc.__reason = values.reason;
            frm.doc.__posting_date = values.posting_date;
            frm.doc.__posting_time = values.posting_time;
        }
        frm.save();
    }
});
