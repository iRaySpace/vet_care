async function get_practitioner_schedules(practitioner, date) {
  const { message: practitioner_schedules } = await frappe.call({
    method: 'vet_care.api.get_practitioner_schedules',
    args: { practitioner, date },
  });
  return practitioner_schedules;
}