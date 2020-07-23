function set_custom_buttons(frm) {
	const custom_buttons = [
		{
			label: __('Book Appointment'),
			onclick: function() {
				frappe.set_route(
                  'List',
                  'Patient Booking',
                  'Calendar',
                  {
                    customer: frm.doc.default_owner,
                    patient: frm.doc.animal,
                  }
                );
			},
		},
	];
	custom_buttons.forEach(function(custom_button) {
		frm.add_custom_button(custom_button['label'], custom_button['onclick']);
	});
}
