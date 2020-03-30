# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe


def execute(filters=None):
	columns = _get_columns(filters)
	data = _get_data(filters)
	return columns, data


def _get_columns(filters):
	def make_column(label, fieldname, width, fieldtype='Data', options=''):
		return {
			'label': _(label),
			'fieldname': fieldname,
			'fieldtype': fieldtype,
			'width': width,
			'options': options
		}
	return [
		make_column('Posting Date', 'posting_date', 130, 'Date'),
		make_column('Activity', 'activity_type', 80, 'Data'),
		make_column('Description', 'description', 893, 'Data')
	]


def _get_data(filters):
	return _get_patient_activity_items(filters.get('patient'))


def _get_patient_activity_items(patient):
	return frappe.db.sql("""
		SELECT
			doc.posting_date,
			item.activity_type,
			item.description
		FROM `tabPatient Activity Item` item
		INNER JOIN `tabPatient Activity` doc ON item.parent = doc.name
		WHERE doc.patient = %s
	""", patient, as_dict=True)
