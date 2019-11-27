frappe.ui.form.on('Sales Invoice', {
    patient: async function(frm) {
        await vet_care.utils.patient_customers_by_pet_relations(frm);
    }
});
