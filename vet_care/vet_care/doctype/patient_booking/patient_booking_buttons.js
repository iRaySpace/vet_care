function set_custom_buttons(frm) {
    const custom_buttons = [
        {
            label: __('Animal Overview'),
            onclick: async function() {
                await frappe.set_route('Form', 'Animal Overview');
                frappe.model.set_value('Animal Overview', 'Animal Overview', 'animal', frm.doc.patient);
            },
        }
    ];
    custom_buttons.forEach((custom_button) => {
        frm.add_custom_button(custom_button['label'], custom_button['onclick']);
    });
}
