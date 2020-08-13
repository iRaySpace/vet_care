function set_custom_buttons(frm) {
    const custom_buttons = [
        {
            label: __('Animal Overview'),
            onclick: async function() {
                const sales_person = await _get_practitioner(frm.doc.physician);
                await frappe.set_route('Form', 'Animal Overview');
                frappe.model.set_value('Animal Overview', 'Animal Overview', 'animal', frm.doc.patient);
                frappe.model.set_value('Animal Overview', 'Animal Overview', 'sales_person', sales_person.employee);
            },
        }
    ];
    custom_buttons.forEach((custom_button) => {
        frm.add_custom_button(custom_button['label'], custom_button['onclick']);
    });
}


async function _get_practitioner(physician) {
    const { message: employee } = await frappe.db.get_value('Healthcare Practitioner', physician, 'employee');
    return employee;
}
