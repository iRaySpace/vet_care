frappe.ui.form.on('Inpatient Record', {
    refresh: async function(frm) {
        await vet_care.utils.patient_customers_by_pet_relations(frm, 'patient', 'vc_customer');
    },
    patient: async function(frm) {
        await vet_care.utils.patient_customers_by_pet_relations(frm, 'patient', 'vc_customer');
    }
});
