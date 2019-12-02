import frappe
from frappe.desk.calendar import get_event_conditions

from toolz import compose, partial


@frappe.whitelist()
def get_events(start, end, filters=None):
    """
    Override ERPNext core's `get_events`
    :param start:
    :param end:
    :param filters:
    :return:
    """
    def get_data(row):
        new_row = row
        new_row['patient'] = ':'.join([
            row.get('patient'),
            row.get('vc_owner'),
            row.get('appointment_type') or 'NA'
        ])
        return new_row

    data = _get_appointment_data(
        get_event_conditions("Patient Appointment", filters),
        {'start': start, 'end': end},
        {'allDay': 0}
    )

    return compose(list, partial(map, get_data))(data)


def _get_appointment_data(conditions, args, update):
    return frappe.db.sql("""
        SELECT
            `tabPatient Appointment`.name,
            `tabPatient Appointment`.patient,
            `tabPatient Appointment`.practitioner,
            `tabPatient Appointment`.status,
            `tabPatient Appointment`.duration,
            `tabPatient Appointment`.appointment_type,
            `tabPatient Appointment`.vc_owner,
            `tabAppointment Type`.color,
            TIMESTAMP(`tabPatient Appointment`.appointment_date, `tabPatient Appointment`.appointment_time) AS start
        FROM `tabPatient Appointment`
        LEFT JOIN `tabAppointment Type` ON `tabPatient Appointment`.appointment_type = `tabAppointment Type`.name
        WHERE `tabPatient Appointment`.appointment_date BETWEEN %(start)s AND %(end)s
        AND `tabPatient Appointment`.status != 'Cancelled'
        AND `tabPatient Appointment`.docstatus < 2
        {conditions}
    """.format(conditions=conditions), args, update=update, as_dict=1)
