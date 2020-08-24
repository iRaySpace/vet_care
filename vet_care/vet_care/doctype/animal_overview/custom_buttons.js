function set_custom_buttons(frm) {
	const custom_buttons = [
		{
		    label: __('Refresh'),
		    onclick: () => _refresh(frm),
		},
		{
		    label: __('View Calendar'),
		    onclick: () => _view_calendar(frm),
		},
		{
			label: __('Book Appointment'),
			onclick: () => _create_patient_booking(frm),
		},
	];
	custom_buttons.forEach(function(custom_button) {
		frm.add_custom_button(custom_button['label'], custom_button['onclick']);
	});
}


function _create_patient_booking(frm) {
    if (!frm.__skip_calendar) {
        frappe.set_route(
            'List',
            'Patient Booking',
            'Calendar',
            {
                customer: frm.doc.default_owner,
                patient: frm.doc.animal,
            }
        );
    } else {
        frappe.model.with_doctype('Patient Booking', function() {
            const doc = frappe.model.get_new_doc('Patient Booking');
            doc.customer = frm.doc.default_owner;
            doc.patient = frm.doc.animal;
            frappe.set_route('Form', 'Patient Booking', doc.name);
        });
    }
}


function _view_calendar(frm) {
    const route_options = {}
    if (frm.doc.default_owner && frm.doc.animal) {
        route_options['customer'] = frm.doc.default_owner;
        route_options['patient'] = frm.doc.animal;
    }
    frappe.set_route(
        'List',
        'Patient Booking',
        'Calendar',
        route_options,
    );
}


function _refresh(frm) {
    const fields = Object.keys(frm.doc);
    const core_fields = [
        'name',
        'owner',
        'creation',
        'modified',
        'modified_by',
        'idx',
        'docstatus',
        '__last_sync_on',
        'doctype',
        '__unsaved',
    ];
    for (const field of fields) {
        if (core_fields.indexOf(field) === -1) {
            frm.set_value(field, null);
        }
    }
    frm.save();
}
