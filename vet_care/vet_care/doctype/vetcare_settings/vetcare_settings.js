// Copyright (c) 2019, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vetcare Settings', {
    apply_core_overrides: async function(frm) {
        const { message: data } = await frappe.call({ method: 'vet_care.api.apply_core_overrides' });
        frappe.msgprint(`Overrided core: ${JSON.stringify(data)}`);
    }
});
