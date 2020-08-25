# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from toolz.curried import compose, groupby, valmap, first


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
		make_column('Invoice No', 'invoice_no', 130, 'Link', 'Sales Invoice'),
		make_column('Invoice Date', 'invoice_date', 130, 'Date'),
		make_column('Item', 'item', 130, 'Link', 'Item'),
		make_column('Item Group', 'item_group', 130, 'Link', 'Item Group'),
		make_column('Description', 'description', 130),
		make_column('Total VAT', 'total_vat', 130, 'Currency'),
		make_column('Cost Center', 'cost_center', 130, 'Link', 'Cost Center'),
		make_column('Customer', 'customer', 130, 'Link', 'Customer'),
		make_column('Customer Name', 'customer_name', 130, 'Data'),
		make_column('Patient', 'patient', 130, 'Link', 'Patient'),
		make_column('Patient Name', 'patient_name', 130, 'Data'),
		make_column('Species', 'species', 130, 'Data')
	]


def _get_clauses(filters):
	clauses = [
		'si.docstatus = 1',
		'si.posting_date BETWEEN %(from_date)s AND %(to_date)s'
	]
	return 'WHERE {}'.format(' AND '.join(clauses))


def _get_data(filters):
	def make_data(row):
		rate = _get_rate(row.get('taxes_and_charges'), cached_taxes_and_charges) / 100.00
		row['total_vat'] = row.get('amount') * rate
		row['species'] = species.get(row.get('patient'))
		return row
	data = frappe.db.sql("""
		SELECT
			si.name as invoice_no,
			si.posting_date as invoice_date,
			sii.item_code as item,
			i.item_group,
			sii.description,
			sii.amount,
			si.taxes_and_charges,
			sii.cost_center,
			si.customer,
			si.customer_name,
			si.patient,
			si.patient_name
		FROM `tabSales Invoice Item` sii
		INNER JOIN `tabSales Invoice` si ON si.name = sii.parent
		INNER JOIN `tabItem` i ON i.name = sii.item_code
		{clauses}
	""".format(clauses=_get_clauses(filters)), filters, as_dict=1)
	cached_taxes_and_charges = {}
	species = _get_species(list(set(map(lambda x: x['patient'], data))))
	return list(map(make_data, data))


def _get_rate(template, cache=None):
	if cache and template in cache:
		return cache[template]

	if template is None:
		return 0.00

	taxes_and_charges = frappe.get_all(
		'Sales Taxes and Charges',
		filters={'parent': template},
		fields=['rate']
	)

	rate = 0.0
	if taxes_and_charges:
		rate = taxes_and_charges[0].get('rate')

	if cache is not None:
		cache[template] = rate

	return rate


def _get_species(patients):
	species = compose(
		valmap(lambda x: x['vc_species']),
		valmap(first),
		groupby('name'),
		lambda: frappe.get_all(
			'Patient',
			filters=[['name', 'in', patients]],
			fields=['name', 'vc_species']
		)
	)
	return species()
