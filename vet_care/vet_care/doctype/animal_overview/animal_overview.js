// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

frappe.ui.form.on('Animal Overview', {
	refresh: function(frm) {
		frm.disable_save();
		_set_actions(frm);
	},
	animal: function(frm) {
		_set_animal_details(frm);
		_set_clinical_history(frm);
	}
});

frappe.ui.form.on('Animal Overview Item', {
	qty: function(frm, cdt, cdn) {
		_update_child_amount(frm, cdt, cdn);
	},
	rate: function(frm, cdt, cdn) {
		_update_child_amount(frm, cdt, cdn);
	},
	item_code: async function(frm, cdt, cdn) {
		const child = _get_child(cdt, cdn);

		if (!child.qty) {
			frappe.model.set_value(cdt, cdn, 'qty', 1.0);
		}

		if (!child.rate) {
			const { message: item } = await frappe.db.get_value(
				'Item',
				{ name: child.item_code },
				'standard_rate',
			);
			frappe.model.set_value(cdt, cdn, 'rate', item.standard_rate);
		}
	},
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
	// const { message: medical_records } = await frappe.call({
	// 	method: 'vet_care.api.get_medical_records',
	// 	args: { patient: frm.doc.animal }
	// });

	const { message: clinical_history } = await frappe.call({
		method: 'vet_care.api.get_clinical_history',
		args: { patient: frm.doc.animal }
	});

	const fields = ['posting_date', 'description', 'price'];

	const table_rows = _get_table_rows(clinical_history, fields);
	const table_header = _get_table_header(fields);
	$(frm.fields_dict['clinical_history_html'].wrapper).html(`
		<table class="table table-bordered">
			${table_header}
			${table_rows.join('\n')}
		</table>
	`);
}

function _set_actions(frm) {
	$(frm.fields_dict['actions_html'].wrapper).html(`
		<div class="row">
			<div class="col-sm-6">
				<button class="btn btn-xs btn-primary" id="close">Close</button>
				<button class="btn btn-xs btn-danger" id="discard">Discard</button>
			</div>
		</div>
	`);

	const actions = {
		close: function() {
			frappe.confirm(
				'Are you sure you want to close the invoice?',
				() => _close_invoice(frm),
			);
		},
		discard: function() {
			frm.set_value('items', []);
		}
	};

	_map_buttons_to_functions(actions, {
		decorator_fn: (fn) => {
			if (!frm.doc.animal) {
				frappe.throw(__('Animal is required.'));
				return;
			}
			fn();
		},
	});
}

function _update_child_amount(frm, cdt, cdn) {
	const child = _get_child(cdt, cdn);
	frappe.model.set_value(cdt, cdn, 'amount', child.qty * child.rate);
}

async function _close_invoice(frm) {
	const { message: invoice } = await frappe.call({
		method: 'vet_care.api.close_invoice',
		args: {
			items: frm.doc.items,
			patient: frm.doc.animal,
			customer: frm.doc.default_owner,
		},
	});
	frappe.show_alert(`Sales Invoice ${invoice.name} created`);
	frm.set_value('items', []);
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

// actions utils
function _map_buttons_to_functions(actions, args) {
	const decorator_fn = args.decorator_fn
		? args.decorator_fn
		: null;
	Object.keys(actions).forEach((action) => {
		$(`#${action}`).click(
			decorator_fn
				? () => decorator_fn(actions[action])
				: actions[action]
		);
	});
}

// child table utils
function _get_child(cdt, cdn) {
	return locals[cdt][cdn];
}
