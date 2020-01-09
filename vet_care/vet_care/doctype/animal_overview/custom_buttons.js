function set_custom_buttons(frm) {
	const custom_buttons = [
		{
			label: __('Make Appointment'),
			onclick: function() {
				frappe.set_route('List', 'Patient Appointment', 'Calendar');
			},
		},
		{
			label: __('Save to Patient'),
			onclick: async function() {
				if (!frm.doc.animal) {
					frappe.throw(__('Animal is required'));
				}
				await frappe.call({
					method: 'vet_care.api.save_to_patient',
					args: {
					  patient: frm.doc.animal,
            data: {
					    patient_name: frm.doc.animal_name,
              sex: frm.doc.sex,
              dob: frm.doc.dob,
              vc_color: frm.doc.color,
              vc_weight: frm.doc.weight,
              vc_species: frm.doc.species,
              vc_breed: frm.doc.breed,
            },
          },
				});
				frappe.msgprint('Successfully saved to Patient', 'Save Patient');
			},
		},
	];
	custom_buttons.forEach(function(custom_button) {
		frm.add_custom_button(custom_button['label'], custom_button['onclick']);
	});
}

