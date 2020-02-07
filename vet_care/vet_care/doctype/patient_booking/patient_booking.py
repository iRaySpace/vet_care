# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe import _
from frappe.utils import get_datetime
from frappe.model.document import Document
from toolz import compose, partial
from vet_care.api import get_practitioner_schedules


class PatientBooking(Document):
	def validate(self):
		_validate_appointment_times(self)
		_set_names(self)


def _validate_appointment_times(doc):
	practitioner_schedules = get_practitioner_schedules(doc.physician, doc.appointment_date)
	appointment_time = get_datetime(doc.appointment_time).strftime('%H:%M')
	if appointment_time not in practitioner_schedules:
		frappe.throw(_('Selected appointment time is not available'))


def _set_names(doc):
	doc.customer_name = frappe.get_value('Customer', doc.customer, 'customer_name')
	doc.patient_name = frappe.get_value('Patient', doc.patient, 'patient_name')
	doc.physician_name = frappe.get_value('Healthcare Practitioner', doc.physician, 'last_name')


@frappe.whitelist()
def get_events(start, end, filters=None):
	"""
	Returns events for Gantt / Calendar view rendering.
	:param start:
	:param end:
	:param filters:
	:return: {'name', 'title', 'start', 'end'}
	"""
	def get_color_data(practitioner):
		return frappe.get_value('Healthcare Practitioner', practitioner, 'vc_color')

	def get_data(data):
		return {
			'allDay': 0,
			'name': data.get('name'),
			'start': data.get('start'),
			'end': data.get('start') + datetime.timedelta(minutes=30.0),
			'color': get_color_data(data.get('physician')) or '#EFEFEF',
			'title': '; '.join([
				data.get('customer_name') or 'NA',
				data.get('patient_name') or 'NA',
				data.get('physician_name') or 'NA'
			])
		}

	args = {
		'start': start,
		'end': end
	}

	return compose(
		partial(map, get_data)
	)(
		frappe.db.sql("""
			SELECT
				pb.name,
				pb.customer_name,
				pb.patient_name,
				pb.physician_name,
				pb.physician,
				TIMESTAMP(pb.appointment_date, pb.appointment_time) as start
			FROM `tabPatient Booking` pb
			WHERE (pb.appointment_date BETWEEN %(start)s AND %(end)s)
			AND pb.docstatus < 2
		""", args, as_dict=True)
	)
