# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
import json
from frappe import _
from frappe.utils import get_datetime
from frappe.model.document import Document
from toolz import compose, partial
from vet_care.api import get_practitioner_schedules


class PatientBooking(Document):
	def validate(self):
		_validate_out_of_clinic(self)
		_validate_appointment_times(self)
		_set_names(self)


def _validate_out_of_clinic(doc):
	out_of_clinic = frappe.db.get_value('Healthcare Practitioner', doc.physician, 'vc_out_of_clinic')
	if out_of_clinic:
		frappe.throw(_('Physician is out of clinic. Please try again later.'))


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
		appointment_minutes = data.get('appointment_minutes') or 30.0
		return {
			'allDay': 0,
			'name': data.get('name'),
			'start': data.get('start'),
			'end': data.get('start') + datetime.timedelta(minutes=appointment_minutes),
			'color': get_color_data(data.get('physician')) or '#EFEFEF',
			'title': '; '.join([
				data.get('customer_name') or 'NA',
				data.get('patient_name') or 'NA',
				data.get('physician_name') or 'NA',
				data.get('appointment_type') or 'NA'
			])
		}

	return compose(
		partial(map, get_data)
	)(
		frappe.get_all(
			'Patient Booking',
			fields=[
				'name',
				'customer_name',
				'patient_name',
				'physician_name',
				'physician',
				'appointment_type',
				'appointment_minutes',
				'TIMESTAMP(appointment_date, appointment_time) as start'
			],
			filters=[
				*_get_clauses(filters),
				['appointment_date', 'Between', [start, end]]
			]
		)
	)


def _get_clauses(filters):
	def make_data(filter):
		if len(filter) > 4:
			filter.pop()
		return filter
	filters = json.loads(filters)
	return list(map(make_data, filters))
