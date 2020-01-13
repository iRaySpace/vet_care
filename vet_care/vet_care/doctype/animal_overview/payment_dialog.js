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
					fieldname: 'amount_due',
					fieldtype: 'Currency',
					label: __('Amount Due'),
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

		dialog.set_primary_action('Submit & Pay', function() {
			dialog.hide();
			resolve(dialog.get_values());
		});

		// Initialize dialog
		dialog.set_value('patient', frm.doc.animal);
		dialog.set_value('patient_name', frm.doc.animal_name);
		dialog.set_value('customer', frm.doc.default_owner);
		dialog.set_value('amount_due', frm.doc.items.reduce((total, item) => total + item.amount, 0.00));
		dialog.show();
	});
}
