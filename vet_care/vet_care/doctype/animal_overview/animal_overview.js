// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt

{% include 'vet_care/vet_care/doctype/animal_overview/data.js' %}
{% include 'vet_care/vet_care/doctype/animal_overview/print.js' %}
{% include 'vet_care/vet_care/doctype/animal_overview/payment_dialog.js' %}
{% include 'vet_care/vet_care/doctype/animal_overview/custom_buttons.js' %}

let _filter_length = 20;
let _tax_rate = 0;

frappe.ui.form.on('Animal Overview', {
    onload: function(frm) {
        frm.set_query('default_owner', function() {
            return {
                query: "erpnext.controllers.queries.customer_query",
            };
        });
        get_tax_rate().then((data) => _tax_rate = data);
        get_skip_calendar().then((skip_calendar) => frm.__skip_calendar = skip_calendar);
        get_selling_price_list().then((selling_price_list) => frm.__selling_price_list = selling_price_list);
        get_show_zip_code().then((show_zip_code) => {
            // read only fields can't be set through set_df_property
            if (!show_zip_code) {
                $('div[title="zip_code"]').hide();
            }
        });
    },
    refresh: function(frm) {
        if (frappe.route_options && frappe.route_options.animal) {
            frm.set_value('animal', frappe.route_options.animal);
            frappe.route_options = {};
        }
        frm.disable_save();
        set_custom_buttons(frm);
        _set_actions(frm);
        _set_form_buttons_color();
        _set_attach_read_only(frm);
    },
    inpatient: async function(frm) {
        if (!frm.doc.animal || frm.doc.__init) return;
        if (frm.doc.inpatient) {
            const values = await vet_care.utils.prompt_admission_dialog();
            frm.doc.__new_patient_activity = true;
            frm.doc.__reason = values.reason;
            frm.doc.__posting_date = values.posting_date;
            frm.doc.__posting_time = values.posting_time;
        } else {
            const values = await vet_care.utils.prompt_discharge_dialog();
            frm.doc.__new_patient_activity = true;
            frm.doc.__reason = values.reason;
            frm.doc.__posting_date = values.posting_date;
            frm.doc.__posting_time = values.posting_time;
        }
        await save_patient(frm);
        _set_clinical_history(frm);
    },
    save_patient: async function(frm) {
        if (frm.doc.is_new_patient) {
            await make_patient(frm);
        } else {
            await save_patient(frm);
        }
    },
    animal: function(frm) {
        _set_animal_details(frm);
        _set_clinical_history(frm);
        _set_invoice_query(frm);
        _set_attach_read_only(frm);
    },
    invoice: async function(frm) {
        if (frm.doc.invoice) {
            const items = await get_invoice_items(frm.doc.invoice);
            frm.set_value('items', items);
            _update_taxes_and_charges(frm);
            _update_total(frm);
        }
    },
    default_owner: async function(frm) {
        _set_default_owner_query(frm);
        if (frm.doc.default_owner && !frm.doc.animal) {
            _clear_animal_details(frm);
            const animal = await get_first_animal_by_owner(frm.doc.default_owner);
            if (animal) frm.set_value('animal', animal.name);
        }
    },
    is_new_patient: function(frm) {
        if (frm.doc.is_new_patient) {
            _clear_animal_details(frm);
        }
        frm.set_df_property('animal', 'read_only', frm.doc.is_new_patient);
        frm.set_df_property('inpatient', 'hidden', frm.doc.is_new_patient);
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
            'vs_weight:weight',
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

        const patient_activity = await make_patient_activity(
            frm.doc.animal,
            frm.doc.activity_items,
            frm.doc.sales_person,
        );
        frappe.show_alert(`Patient Activity ${patient_activity.name} created`);
        frm.set_value('activity_items', []);
        frm.save();

        // refresh clinical history
        _set_clinical_history(frm);
    },
    // TODO: make a decorator for above
    new_print_activity: async function(frm) {
      if (!frm.doc.animal) {
            frappe.throw(__('Animal is required.'));
            return;
        }

        const patient_activity = await make_patient_activity(
            frm.doc.animal,
            frm.doc.activity_items,
            frm.doc.physician,
        );
        frappe.show_alert(`Patient Activity ${patient_activity.name} created`);
        print_activity(frm);

        frm.activity_items = [...frm.doc.activity_items];
        frm.set_value('activity_items', []);

        // refresh clinical history
        _set_clinical_history(frm);
    },
    discount_per: function(frm) {
      const subtotal = _get_subtotal(frm);
      const discount_amount = subtotal * (frm.doc.discount_per / 100.00);
      frm.set_value('discount_amount', discount_amount);
    },
    discount_amount: function(frm) {
      _update_total(frm);
    },
    print_history: function(frm) {
      print_history(frm);
    },
});

frappe.ui.form.on('Animal Overview Item', {
	qty: function(frm, cdt, cdn) {
		_update_child_amount(frm, cdt, cdn);
		_update_taxes_and_charges(frm);
		_update_total(frm);
	},
	rate: function(frm, cdt, cdn) {
		_update_child_amount(frm, cdt, cdn);
		_update_taxes_and_charges(frm);
		_update_total(frm);
	},
	item_code: async function(frm, cdt, cdn) {
		const child = _get_child(cdt, cdn);
		if (!child.qty) {
			frappe.model.set_value(cdt, cdn, 'qty', 1.0);
		}
		if (!child.rate) {
			const item_rate = await get_item_rate(child.item_code, frm.__selling_price_list);
			frappe.model.set_value(cdt, cdn, 'rate', item_rate);
		}
	},
	items_remove: function(frm) {
	  _update_taxes_and_charges(frm);
      _update_total(frm);
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
		['inpatient', 'vc_inpatient']
	];
  if (frm.doc.animal) {
    patient = await frappe.db.get_doc('Patient', frm.doc.animal);
    frm.set_value('default_owner', patient.customer);
    frm.doc.__init = true;
  }
  for (const field of fields) {
    await frm.set_value(field[0], patient ? patient[field[1]] : '');
  }
  frm.doc.__init = false;
}


function _set_attach_read_only(frm) {
  frm.set_df_property('attach', 'read_only', frm.doc.animal ? 0 : 1);
}


// TODO: move out to other js
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

// TODO: move to utils
function _clear_vital_signs(frm) {
	const fields = [
		'temperature',
		'pulse',
		'respiratory_rate',
		'mucous_membrane',
		'capillary_refill_time',
		'vs_weight',
	];
	fields.forEach((field) => frm.set_value(field, ''));
}

async function _set_clinical_history(frm) {
	const clinical_history = await get_clinical_history(frm.doc.animal, _filter_length);
	frm.clinical_history = clinical_history;

	const fields = ['posting_date', 'name', 'description', 'price'];

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
				<button class="btn btn-xs btn-primary" id="save">Save</button>
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

			const invoice = await save_invoice(
			    frm.doc.items,
			    frm.doc.animal,
			    frm.doc.default_owner,
			    frm.doc.sales_person,
                frm.doc.invoice,
                frm.doc.discount_amount,
            );
			frappe.show_alert(`Sales Invoice ${invoice.name} saved`);

			frm.set_value('items', []);
		},
		pay: async function() {
			if (!frm.doc.invoice) {
				frappe.throw(__('Please select invoice above'));
			}

			await save_invoice(
			    frm.doc.items,
			    frm.doc.animal,
			    frm.doc.default_owner,
			    frm.doc.sales_person,
                frm.doc.invoice,
                frm.doc.discount_amount,
            );

			const values = await show_payment_dialog(frm);
			if (!values.payments) {
			  frappe.throw(__('No payments found. Please put payment details.'));
			}

			const invoice = await pay_invoice(frm.doc.invoice, values.payments);
			frappe.show_alert(`Sales Invoice ${invoice.name} paid`);

            if (values.__print) {
              _print_doc('Sales Invoice', invoice.name, 'Standard', 0);
            }

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

function _update_taxes_and_charges(frm) {
  const vat_amounts = frm.doc.items.map(function(item) {
    return item.amount * (_tax_rate / 100.00);
  });
  frm.set_value('taxes_and_charges', vat_amounts.reduce((total, vat_amount) => total + vat_amount, 0.00));
}

function _update_total(frm) {
  const subtotal = _get_subtotal(frm);
  const total = [
    subtotal
    -frm.doc.discount_amount
  ];
  frm.set_value('total', total.reduce((grand_total, value) => grand_total + value, 0.00));
}

function _get_subtotal(frm) {
  const amounts = frm.doc.items.map(function(item) {
    return item.amount;
  });
  const total = [
    amounts.reduce((total, amount) => total + amount, 0.00),
    frm.doc.taxes_and_charges
  ];
  return total.reduce((subtotal, value) => subtotal + value, 0.00);
}

// table utils
function _get_table_rows(records, fields) {
	return records.map((record) => {
		if (!fields)
			fields = Object.keys(record);
		const table_data = fields.map((field) => {
			if (field === 'description') {
			    const attach = record['attach']
			        ? `<a href=${record['attach']} class="btn btn-default btn-xs" target="_blank">See attached</a>`
			        : '';
				return `
					<td>
						<pre style="font-family: 'serif'">${record[field]}</pre>
						${attach}
					</td>
				`;
			}
			if (field === 'name') {
			    const ref_type = record['ref_type'] === 'pa'
			        ? 'Patient%20Activity'
			        : 'Sales%20Invoice';
			    const link = `/desk#Form/${ref_type}/${record[field]}`;
			    return `
			        <td>
			            <a href=${link}>${record[field]}</a>
			        </td>
			    `;
			}
			return `<td>${record[field]}</td>`;
		});
		return `<tr>${table_data.join('\n')}</tr>`;
	});
}

function _get_table_header(fields) {
    // correspondingly
    // posting_date, name, description, price
    const width = ['10%', '10%', '55%', '15%'];
	const header_texts = fields.map((field) =>
		field.split('_')
			.map((s) => s.charAt(0).toUpperCase() + s.substring(1))
			.join(' ')
	);
	const columns = header_texts.map((column, index) =>
		`<th width=${width[index]}>${column}</th>`);
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

// other utils
function _set_form_buttons_color() {
    $('button[data-fieldname="new_activity"]').addClass('btn-primary');
    $('button[data-fieldname="vs_save"]').addClass('btn-primary');
    $('button[data-fieldname="save_patient"]').addClass('btn-primary');
}


function _print_doc(doctype, docname, print_format, no_letterhead) {
  // from /frappe/public/js/frappe/form/print.js
  const w = window.open(
    frappe.urllib.get_full_url(
      `/printview?doctype=${encodeURIComponent(doctype)}&name=${encodeURIComponent(
        docname
      )}&trigger_print=1&format=${encodeURIComponent(print_format)}&no_letterhead=${
        no_letterhead ? '1' : '0'
      }&_lang=en`
    )
  );
  if (!w) {
    frappe.msgprint(__('Please enable pop-ups'));
  }
}
