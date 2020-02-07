// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt
{% include 'vet_care/vet_care/doctype/animal_overview/data.js' %}
{% include 'vet_care/vet_care/doctype/animal_overview/payment_dialog.js' %}
{% include 'vet_care/vet_care/doctype/animal_overview/custom_buttons.js' %}

let _filter_length = 20;

frappe.ui.form.on('Animal Overview', {
	onload: function(frm) {
		frm.set_query('default_owner', function() {
			return {
				query: "erpnext.controllers.queries.customer_query",
			};
		});
	},
	refresh: function(frm) {
		frm.disable_save();
		set_custom_buttons(frm);
		_set_actions(frm);
		// _set_fields_read_only(frm, true);
	},
	animal: function(frm) {
		_set_animal_details(frm);
		_set_clinical_history(frm);
		_set_invoice_query(frm);
		// _set_fields_read_only(frm, !frm.doc.animal);
	},
	invoice: async function(frm) {
		if (frm.doc.invoice) {
			const items = await get_invoice_items(frm.doc.invoice);
			frm.set_value('items', items);
			frm.set_df_property('items', 'read_only', true);
		}
	},
  default_owner: async function(frm) {
		_set_default_owner_query(frm);
		if (frm.doc.default_owner) {
			_clear_animal_details(frm);
			const animal = await get_first_animal_by_owner(frm.doc.default_owner);
			if (animal) frm.set_value('animal', animal.name);
			const { message: customer } = await frappe.db.get_value(
				'Customer',
				{ 'name': frm.doc.default_owner },
				'customer_name'
			);
			if (customer) frm.set_value('owner_name', customer.customer_name);
		}
  },
	is_new_patient: function(frm) {
		if (frm.doc.is_new_patient) {
			_clear_animal_details(frm);
		}
		frm.set_df_property('animal', 'read_only', frm.doc.is_new_patient);
	},
	vs_save: async function(frm) {
		if (!frm.doc.animal) {
			frappe.throw(__('Animal is required'));
		}
		const fields = [
			'temperature',
			'pulse',
			'respiratory_rate',
			'mucous_membrane',
			'capillary_refill_time',
			'vs_height:height',
			'vs_weight:weight',
			'notes'
		];

		const data = fields.reduce(function(dict, x) {
			const words = x.split(':');
			dict[words[words.length - 1]] = frm.doc[words[0]];
			return dict;
		}, {});

		const vital_signs = await make_vital_signs(frm.doc.animal, data);
		frappe.show_alert(`Vital Signs ${vital_signs.name} created`);

		_clear_vital_signs(frm);
		_set_clinical_history(frm);
	},
	new_activity: async function(frm) {
		if (!frm.doc.animal) {
			frappe.throw(__('Animal is required.'));
			return;
		}

		const patient_activity = await make_patient_activity(frm.doc.animal, frm.doc.activity_items);
		frappe.show_alert(`Patient Activity ${patient_activity.name} created`);

		// clear data
		// frm.set_value('activity_type', '');
		// frm.set_value('description', '');
		frm.set_value('activity_items', []);

		// refresh clinical history
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
			const { message: item } = await get_item_rate(child.item_code);
			frappe.model.set_value(cdt, cdn, 'rate', item.standard_rate);
		}
	},
});

function _set_invoice_query(frm) {
	frm.set_query('invoice', function(doc, cdt, cdn) {
		return {
			filters: {
				'status': 'Draft',
				'patient': frm.doc.animal,
			}
		};
	});
}

// TODO: put as utils
function _set_default_owner_query(frm) {
  frm.set_query('animal', function(doc, cdt, cdn) {
    return {
      filters: { 'customer': frm.doc.default_owner ? frm.doc.default_owner : null }
    }
  });
}

async function _set_animal_details(frm) {
  let patient;
  const fields = [
		['animal_name', 'patient_name'],
		['dob', 'dob'],
		['weight', 'vc_weight'],
		['sex', 'sex'],
		['breed', 'vc_breed'],
		['species', 'vc_species'],
		['color', 'vc_color'],
		['chip_id', 'vc_chip_id'],
		['neutered', 'vc_neutered'],
	];
  if (frm.doc.animal) {
    patient = await frappe.db.get_doc('Patient', frm.doc.animal);
    frm.set_value('default_owner', patient.customer);
  }
  fields.forEach((field) => frm.set_value(field[0], patient ? patient[field[1]] : ''));
}

function _clear_animal_details(frm) {
	const fields = [
		'animal',
		'animal_name',
		'dob',
		'weight',
		'sex',
		'breed',
		'species',
		'color',
	];
	fields.forEach((field) => frm.set_value(field, ''));
}

function _clear_vital_signs(frm) {
	const fields = [
		'temperature',
		'pulse',
		'respiratory_rate',
		'mucous_membrane',
		'capillary_refill_time',
		'vs_height',
		'vs_weight',
		'notes'
	];
	fields.forEach((field) => frm.set_value(field, ''));
}

async function _set_clinical_history(frm) {
	const clinical_history = await get_clinical_history(frm.doc.animal, _filter_length);
	const fields = ['posting_date', 'description', 'price'];

	const table_rows = _get_table_rows(clinical_history, fields);
	const table_header = _get_table_header(fields);

	// TODO: separate to renderer
	$(frm.fields_dict['clinical_history_html'].wrapper).html(`
		<table class="table table-bordered">
			${table_header}
			${table_rows.join('\n')}
		</table>
		<div class="list-paging-area level">
			<div class="btn-group">
				<button class="btn btn-default btn-paging" data-value="20">20</button>
				<button class="btn btn-default btn-paging" data-value="100">100</button>
				<button class="btn btn-default btn-paging" data-value="500">500</button>
			</div>
			<div>
				<button class="btn btn-default btn-more">More...</button>
			</div>
		</div>
	`);

	_set_clinical_history_buttons(frm);
}

function _set_clinical_history_buttons(frm) {
	$('.btn-paging').click(function() {
		_filter_length = $(this).data('value');
		_set_clinical_history(frm);
	});
}

function _set_actions(frm) {
	$(frm.fields_dict['actions_html'].wrapper).html(`
		<div class="row">
			<div class="col-sm-6">
				<button class="btn btn-xs" style="background-color: #03a9f4" id="save">Save</button>
				<button class="btn btn-xs" style="background-color: #8bc34a" id="pay">Pay</button>
				<button class="btn btn-xs btn-danger" id="discard">Discard</button>
			</div>
		</div>
	`);

	const actions = {
		save: async function() {
			if (!frm.doc.items.length) {
				frappe.throw(__('Items are required'));
			}

			const invoice = await save_invoice(frm.doc.items, frm.doc.animal, frm.doc.default_owner);
			frappe.show_alert(`Sales Invoice ${invoice.name} saved`);

			frm.set_value('items', []);
		},
		pay: async function() {
			if (!frm.doc.invoice) {
				frappe.throw(__('Please select invoice above'));
			}

			const values = await show_payment_dialog(frm);
			const invoice = await pay_invoice(frm.doc.invoice, values.payments);
			frappe.show_alert(`Sales Invoice ${invoice.name} paid`);

			frm.set_value('invoice', '');
			frm.set_value('items', []);

			// reload clinical history
			_set_clinical_history(frm);
		},
		discard: function() {
			frm.set_value('invoice', '');
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

// table utils
function _get_table_rows(records, fields) {
	return records.map((record) => {
		if (!fields)
			fields = Object.keys(record);
		const table_data = fields.map((field) => {
			if (field === 'description') {
				return `
					<td>
						<pre style="font-family: 'serif'">${record[field]}</pre>
					</td>
				`;
			}
			return `<td>${record[field]}</td>`;
		});
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
