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
            const values = await _admission_dialog();
            frm.doc.__new_patient_activity = true;
            frm.doc.__reason = values.reason;
            frm.doc.__posting_date = values.posting_date;
            frm.doc.__posting_time = values.posting_time;
        } else {
            const values = await _discharge_dialog();
            frm.doc.__new_patient_activity = true;
            frm.doc.__reason = values.reason;
            frm.doc.__posting_date = values.posting_date;
            frm.doc.__posting_time = values.posting_time;
        }
        frm.save();
    }
});

async function _admission_dialog() {
    return new Promise((resolve, reject) => {
        const d = new frappe.ui.Dialog({
            title: 'Patient Admission',
            primary_action: function() {
                d.hide();
                resolve(d.get_values());
            },
            fields: [
                {
                    fieldname: 'reason',
                    fieldtype: 'Small Text',
                    label: __('Reason'),
                    required: 1,
                },
                { fieldtype: 'Section Break' },
                {
                    fieldname: 'posting_date',
                    fieldtype: 'Date',
                    label: __('Posting Date'),
                    required: 1,
                },
                { fieldtype: 'Column Break' },
                {
                    fieldname: 'posting_time',
                    fieldtype: 'Time',
                    label: __('Posting Time'),
                    required: 1,
                },
            ],
        });
        d.set_value('posting_date', frappe.datetime.now_date());
        d.set_value('posting_time', frappe.datetime.now_time());
        d.show();
    });
}

async function _discharge_dialog() {
    return new Promise((resolve, reject) => {
        const d = new frappe.ui.Dialog({
            title: 'Patient Discharge',
            primary_action: function() {
                d.hide();
                resolve(d.get_values());
            },
            fields: [
                {
                    fieldname: 'reason',
                    fieldtype: 'Small Text',
                    label: __('Reason'),
                    required: 1,
                },
                { fieldtype: 'Section Break' },
                {
                    fieldname: 'posting_date',
                    fieldtype: 'Date',
                    label: __('Posting Date'),
                    required: 1,
                },
                { fieldtype: 'Column Break' },
                {
                    fieldname: 'posting_time',
                    fieldtype: 'Time',
                    label: __('Posting Time'),
                    required: 1,
                },
            ]
        });
        d.set_value('posting_date', frappe.datetime.now_date());
        d.set_value('posting_time', frappe.datetime.now_time());
        d.show();
    });
}