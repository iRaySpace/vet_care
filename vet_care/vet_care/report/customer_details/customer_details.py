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
		make_column('Customer ID', 'customer_id', 180, 'Link', 'Customer'),
		make_column('Customer Name', 'customer_name', 180, 'Data'),
		make_column('CPR No', 'cpr_no', 130, 'Data'),
		make_column('Mobile Phone', 'mobile_phone', 130, 'Data'),
		make_column('Office Phone', 'office_phone', 130, 'Data'),
		make_column('ID', 'patient_id', 130, 'Link', 'Patient'),
		make_column('Animal Name', 'animal_name', 180, 'Data'),
	]


def _get_data(filters):
	return frappe.db.sql("""
		SELECT
			`tabCustomer`.name as customer_id,
			customer_name as customer_name,
			vc_cpr as cpr_no,
			mobile_number as mobile_phone,
			vc_office_phone as office_phone,
			`tabPatient`.name as patient_id,
			`tabPatient`.patient_name as animal_name
		FROM `tabCustomer`
		INNER JOIN `tabPatient` ON `tabPatient`.customer = `tabCustomer`.name
	""")
