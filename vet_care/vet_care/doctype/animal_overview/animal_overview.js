// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Animal Overview', {
	refresh: function(frm) {
		frm.disable_save();
	},
	animal: async function(frm) {
		const patient = await frappe.db.get_doc('Patient', frm.doc.animal);
		frm.set_value('animal_name', patient.patient_name);
		frm.set_value('species', patient.vc_species);
		frm.set_value('color', patient.vc_color);
		frm.set_value('sex', patient.sex);
		frm.set_value('dob', patient.dob);
		frm.set_value('weight', patient.vc_weight);
		frm.set_value('default_owner', patient.customer);
		frm.set_value('breed', patient.vc_breed);
	}
});
