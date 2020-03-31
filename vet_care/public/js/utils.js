// async function patient_customers_by_pet_relations(frm, patient='patient', customer='customer') {
//     const { message: pet_relations } = await frappe.call({
//         method: 'vet_care.api.get_pet_relations',
//         args: { pet: frm.doc[patient] }
//     });
//     frm.set_query(customer, function() {
//         return {
//             filters: { 'name': ['in', pet_relations] }
//         };
//     });
// }

async function prompt_admission_dialog() {
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

async function prompt_discharge_dialog() {
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

export default {
    patient_customers_by_pet_relations,
    prompt_admission_dialog,
    prompt_discharge_dialog,
};
