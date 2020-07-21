function show_payment_dialog(frm) {
	return new Promise(function(resolve, reject) {
		const mode_of_payments = [];
		const dialog = new frappe.ui.Dialog({
			title: 'Invoice Payment',
			fields: [
				{
					fieldname: 'customer',
					fieldtype: 'Link',
					options: 'Customer',
					label: __('Customer'),
					read_only: 1,
				},
				{
					fieldname: 'payment_cb',
					fieldtype: 'Column Break',
				},
				{
					fieldname: 'patient',
					fieldtype: 'Link',
					options: 'Patient',
					label: __('Patient'),
					read_only: 1,
				},
				{
					fieldname: 'patient_name',
					fieldtype: 'Data',
					label: __('Patient Name'),
					read_only: 1,
				},
				{
					fieldname: 'totals_sb',
					fieldtype: 'Section Break',
				},
				{
					fieldname: 'amount_due',
					fieldtype: 'Currency',
					label: __('Amount Due'),
					read_only: 1,
				},
				{
					fieldname: 'taxes_and_charges',
					fieldtype: 'Currency',
					label: __('Taxes and Charges'),
					read_only: 1,
				},
				{
					fieldname: 'total',
					fieldtype: 'Currency',
					label: __('Total'),
					read_only: 1,
				},
				{
					fieldname: 'payments_sb',
					fieldtype: 'Section Break',
				},
				{
					fieldname: 'payments',
					fieldtype: 'Table',
					fields: [
						{
							fieldname: 'mode_of_payment',
							fieldtype: 'Link',
							options: 'Mode of Payment',
							label: __('Mode of Payment'),
							in_list_view: 1,
						},
						{
							fieldname: 'amount',
							fieldtype: 'Currency',
							label: __('Amount'),
							in_list_view: 1,
						},
					],
					in_place_edit: true,
					data: mode_of_payments,
					get_data: () => mode_of_payments,
				},
			],
		});

		dialog.set_primary_action('Pay & Print', function() {
			dialog.hide();
			resolve({
			  ...dialog.get_values(),
			  __print: true
			});
		});

        _add_button(dialog, 'Pay', function() {
            dialog.hide();
            resolve(dialog.get_values());
        });

		// Initialize dialog
		dialog.set_value('patient', frm.doc.animal);
		dialog.set_value('patient_name', frm.doc.animal_name);
		dialog.set_value('customer', frm.doc.default_owner);
		dialog.set_value('amount_due', frm.doc.items.reduce((total, item) => total + item.amount, 0.00));
		dialog.set_value('taxes_and_charges', frm.doc.taxes_and_charges);
		dialog.set_value('total', frm.doc.total);
		dialog.show();
	});
}


function _add_button(dialog, label, click) {
  const $primary_btn = dialog.get_primary_btn();
  const $button = $(`
    <button type="button" class="btn btn-default btn-sm">${label}</button>
  `);
  $button.insertBefore($primary_btn);
  $button.on('click', click);
}
