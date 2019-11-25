frappe.ui.form.on('Sales Invoice', {
    patient: async function(frm) {
        const { message: pet_relations } = await frappe.call({
            method: "vet_care.api.get_pet_relations",
            args: { pet: frm.doc.patient }
        });
        frm.set_query('customer', function() {
            return {
                query: 'erpnext.controllers.queries.customer_query',
                filters: { 'name': ['in', pet_relations] }
            };
        });
    }
});
