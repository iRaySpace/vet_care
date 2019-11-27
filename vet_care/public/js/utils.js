async function patient_customers_by_pet_relations(frm, patient='patient', customer='customer') {
    const { message: pet_relations } = await frappe.call({
        method: 'vet_care.api.get_pet_relations',
        args: { pet: frm.doc[patient] }
    });
    frm.set_query(customer, function() {
        return {
            filters: { 'name': ['in', pet_relations] }
        };
    });
}

export default {
    patient_customers_by_pet_relations
};
