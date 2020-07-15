async function save_invoice(items, patient, customer, existing_invoice) {
    console.log(existing_invoice);
    const { message: invoice } = await frappe.call({
		method: 'vet_care.api.save_invoice',
		args: { items, patient, customer, existing_invoice },
	});
    return invoice;
}

async function pay_invoice(invoice, payments) {
	const { message: sales_invoice } = await frappe.call({
		method: 'vet_care.api.pay_invoice',
		args: { invoice, payments },
	});
	return sales_invoice;
}

async function get_invoice_items(invoice) {
	const { message: items } = await frappe.call({
		method: 'vet_care.api.get_invoice_items',
		args: { invoice },
	});
	return items;
}

async function get_clinical_history(patient, filter_length) {
    if (!patient) return [];
	const { message: clinical_history } = await frappe.call({
		method: 'vet_care.api.get_clinical_history',
		args: { patient, filter_length },
	});
    return clinical_history;
}

async function make_patient_activity(patient, activity_items) {
  const { message: patient_activity } = await frappe.call({
    method: 'vet_care.api.make_patient_activity',
    args: { patient, activity_items },
  });
  return patient_activity;
}

async function make_vital_signs(patient, data) {
	const { message: vital_signs } = await frappe.call({
		method: 'vet_care.api.make_vital_signs',
		args: { patient, vital_signs: data },
	});
	return vital_signs;
}

function get_item_rate(name) {
	return frappe.db.get_value('Item', { name }, 'standard_rate');
}

async function get_first_animal_by_owner(owner) {
	const { message: animal } = await frappe.call({
		method: 'vet_care.api.get_first_animal_by_owner',
		args: { owner },
	});
	return animal;
}

async function get_tax_rate() {
  const { message: tax_rate } = await frappe.call({
      method: 'vet_care.api.get_tax_rate',
  });
  return tax_rate;
}

async function make_patient(frm) {
	const { message: patient } = await frappe.call({
		method: 'vet_care.api.make_patient',
		args: {
			owner: frm.doc.default_owner,
			patient_data: {
				patient_name: frm.doc.animal_name,
				sex: frm.doc.sex,
				dob: frm.doc.dob,
				vc_color: frm.doc.color,
				vc_weight: frm.doc.weight,
				vc_species: frm.doc.species,
				vc_breed: frm.doc.breed,
				vc_chip_id: frm.doc.chip_id,
				vc_neutered: frm.doc.neutered
			},
		},
	});
	frm.set_value('animal', patient.name);
	frm.set_value('is_new_patient', false);
	frappe.msgprint('Successfully added to the Patient list', 'New Patient');
}

async function save_patient(frm) {
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
				vc_chip_id: frm.doc.chip_id,
				vc_neutered: frm.doc.neutered,
				vc_inpatient: frm.doc.inpatient,
				__new_patient_activity: frm.doc.__new_patient_activity,
				__reason: frm.doc.__reason,
				__posting_date: frm.doc.__posting_date,
				__posting_time: frm.doc.__posting_time
			},
		},
	});
	frappe.msgprint('Successfully saved to Patient', 'Save Patient');
}
