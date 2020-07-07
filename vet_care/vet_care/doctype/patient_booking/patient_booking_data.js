// cached no_appointment
let _cached_no_appointment = null;

async function get_practitioner_schedules(practitioner, date) {
  const { message: practitioner_schedules } = await frappe.call({
    method: 'vet_care.api.get_practitioner_schedules',
    args: { practitioner, date },
  });
  return practitioner_schedules;
}

async function get_no_appointment_type() {
  if (!_cached_no_appointment) {
    const { message: no_appointment } = await frappe.call({
      method: 'vet_care.api.get_no_appointment_type',
    });
    _cached_no_appointment = no_appointment;
  }
  return _cached_no_appointment;
}
