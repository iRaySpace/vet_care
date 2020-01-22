// Copyright (c) 2020, 9T9IT and contributors
// For license information, please see license.txt
{% include 'vet_care/vet_care/doctype/patient_booking/patient_booking_data.js' %}

frappe.ui.form.on('Patient Booking', {
	refresh: function(frm) {
		_set_new_frm(frm);
	},
	customer: async function(frm) {
		const { message: customer } = await frappe.db.get_value('Customer', {'name': frm.doc.customer}, 'customer_name');
		frm.set_value('customer_name', customer.customer_name);
	},
	patient: async function(frm) {
		const { message: patient } = await frappe.db.get_value('Patient', {'name': frm.doc.patient}, 'patient_name');
		frm.set_value('patient_name', patient.patient_name);
	},
	physician: async function(frm) {
		const { message: practitioner } = await frappe.db.get_value('Healthcare Practitioner', {'name': frm.doc.physician}, 'last_name');
		frm.set_value('physician_name', practitioner.last_name);
	},
	appointment_date: function(frm) {
		_get_appointment_dates(frm);
		frm.set_value('appointment_time', '00:00:00');
		frm.set_df_property('appointment_time', 'hidden', 1);
	}
});


function _set_new_frm(frm) {
	if (!frm.doc.__islocal) {
		return;
	}
	frm.set_value('posting_date', frappe.datetime.now_date());
	frm.set_df_property('appointment_time', 'hidden', 1);
}


async function _get_appointment_dates(frm) {
		$(frm.fields_dict['appointment_time_html'].wrapper).html(`
		<div class="row">
			<div class="col-sm-12 schedules">
			</div>
		</div>
	`);
	_set_schedules_html(
		await get_practitioner_schedules(
			frm.doc.physician,
			frm.doc.appointment_date)
	);
	$(`.schedule`).click(function() {
		const value = $(this).data('value');
		frm.set_value('appointment_time', value);
		frm.set_df_property('appointment_time', 'hidden', 0);
	});
}


function _set_schedules_html(schedules) {
	if (schedules.length === 0) {
		$('.schedules').append(`
			<p>No available schedules</p>
		`);
	}
	schedules.forEach((schedule) => {
		$('.schedules').append(`
			<button class="btn btn-default schedule" data-value="${schedule}">
				${schedule}
			</button>
		`);
	});
}
