// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Animal Overview', {
	refresh: function(frm) {
		frm.disable_save();
	},
	animal: function(frm) {
		_set_animal_details(frm);
		_set_clinical_history(frm);
	}
});

async function _set_animal_details(frm) {
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

async function _set_clinical_history(frm) {
	const { message: medical_records } = await frappe.call({
		method: 'vet_care.api.get_medical_records',
		args: { patient: frm.doc.animal }
	});

	const fields = ['reference_doctype', 'communication_date'];
	const table_rows = _get_table_rows(medical_records, fields);
	const table_header = _get_table_header(fields);
	$(frm.fields_dict['clinical_history_html'].wrapper).html(`
		<table class="table table-bordered">
			${table_header}
			${table_rows.join('\n')}
		</table>
	`);
}

// table utils
function _get_table_rows(records, fields) {
	return records.map((record) => {
		if (!fields)
			fields = Object.keys(record);
		const table_data = fields.map((field) =>
			`<td>${record[field]}</td>`);
		return `<tr>${table_data.join('\n')}</tr>`;
	});
}

function _get_table_header(fields) {
	const header_texts = fields.map((field) =>
		field.split('_')
			.map((s) => s.charAt(0).toUpperCase() + s.substring(1))
			.join(' ')
	);
	const columns = header_texts.map((column) =>
		`<th>${column}</th>`);
	return `<tr>${columns.join('\n')}</tr>`;
}
