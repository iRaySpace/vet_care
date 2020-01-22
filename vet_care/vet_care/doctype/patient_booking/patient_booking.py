# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document
from toolz import compose, partial


class PatientBooking(Document):
	def validate(self):
		customer_name = frappe.get_value('Customer', self.customer, 'customer_name')
		patient_name = frappe.get_value('Patient', self.patient, 'patient_name')
		practitioner_name = frappe.get_value('Healthcare Practitioner', self.physician, 'last_name')
		self.customer_name = customer_name
		self.patient_name = patient_name
		self.physician_name = practitioner_name


@frappe.whitelist()
def get_events(start, end, filters=None):
	"""
	Returns events for Gantt / Calendar view rendering.
	:param start:
	:param end:
	:param filters:
	:return: {'name', 'title', 'start', 'end'}
	"""
	def get_data(data):
		print(data)
		return {
			'allDay': 0,
			'name': data.get('name'),
			'start': data.get('start'),
			'end': data.get('start') + datetime.timedelta(minutes=30.0),
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
				TIMESTAMP(pb.appointment_date, pb.appointment_time) as start
			FROM `tabPatient Booking` pb
			WHERE (pb.appointment_date BETWEEN %(start)s AND %(end)s)
			AND pb.docstatus < 2
		""", args, as_dict=True)
	)
