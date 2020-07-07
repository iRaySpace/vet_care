# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns, data = _get_columns(filters), _get_data(filters)
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
		make_column('ID', 'patient_id', 130, 'Link', 'Patient'),
		make_column('Animal Name', 'animal_name', 180, 'Data'),
		make_column('Species', 'species', 130, 'Data'),
		make_column('Breed', 'breed', 130, 'Data'),
		make_column('Customer ID', 'customer_id', 90, 'Link', 'Customer'),
		make_column('Customer Name', 'customer_name', 180, 'Data')
	]


def _get_data(filters):
	return frappe.db.sql("""
		SELECT 
			`tabPatient`.name as patient_id,
			patient_name as animal_name,
			vc_species as species,
			vc_breed as breed,
			customer as customer_id,
			`tabCustomer`.customer_name
		FROM `tabPatient`
		INNER JOIN `tabCustomer` ON `tabCustomer`.name = `tabPatient`.customer
	""")
