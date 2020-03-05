frappe.ui.form.on('Patient', {
    onload: function(frm) {
        frm.set_query('customer', 'vc_pet_relation', function() {
            return { query: "erpnext.controllers.queries.customer_query" };
        });
    },
    refresh: function(frm) {
        _add_patient_overview(frm);
        _set_dashboard(frm);
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

function _add_patient_overview(frm) {
    frm.add_custom_button(__('Animal Overview'), function() {
        frappe.route_options = {'animal': frm.doc.name};
        frappe.set_route('Form', 'Animal Overview');
    });
}

function _set_dashboard(frm) {
    const appointments = frm.dashboard.data.transactions.find(({ label }) => label === __('Appointments and Patient Encounters'));
    if (appointments && !appointments.items.includes('Patient')) {
        appointments.items = ['Patient Booking'];
    }

    // Remove Lab Tests and Vital Signs
    const filtered_transactions = frm.dashboard.data.transactions.filter(({ label }) => label !== __('Lab Tests and Vital Signs'));
    frm.dashboard.data.transactions = filtered_transactions;
    frm.dashboard.data_rendered = false;
    frm.dashboard.transactions_area.empty();
    frm.dashboard.refresh();
}
