# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import fmt_money
from toolz.curried import compose, groupby, valmap, first, reduce, unique, pluck, count, partial


def execute(filters=None):
	columns, data = _get_columns(filters), _get_data(filters)
	return columns, _append_summary(data)


def _get_columns(filters):
	def make_column(label, fieldname, width, fieldtype='Data', options='', hidden=False):
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
		make_column('Sales Person', 'sales_person_name', 130, 'Data'),
		make_column('Customer', 'customer', 130, 'Link', 'Customer'),
		make_column('Customer Name', 'customer_name', 130, 'Data'),
		make_column('Patient', 'patient', 130, 'Link', 'Patient'),
		make_column('Patient Name', 'patient_name', 130, 'Data'),
		make_column('Species', 'species', 130, 'Data')
	]


def _get_clauses(filters):
	clauses = list(filter(lambda x: x, [
		'si.docstatus = 1',
		'si.posting_date BETWEEN %(from_date)s AND %(to_date)s',
		'sii.cost_center = %(cost_center)s' if filters.get('cost_center') else None,
	]))
	return 'WHERE {}'.format(' AND '.join(clauses))


def _get_sales_person_fields():
	enable_pb = frappe.db.get_single_value('Vetcare Settings', 'enable_pb')
	if enable_pb:
		fields = [
			'si.pb_sales_employee as sales_person',
			'si.pb_sales_employee_name as sales_person_name'
		]
	else:
		fields = [
			'si.pb_sales_person as sales_person',
			'si.pb_sales_person_name as sales_person_name'
		]
	return ', '.join(fields)


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
			si.patient_name,
			{sales_person_fields}
		FROM `tabSales Invoice Item` sii
		INNER JOIN `tabSales Invoice` si ON si.name = sii.parent
		INNER JOIN `tabItem` i ON i.name = sii.item_code
		{clauses}
	""".format(
		clauses=_get_clauses(filters),
		sales_person_fields=_get_sales_person_fields()
	),
		filters,
		as_dict=1
	)
	cached_taxes_and_charges = {}
	species = _get_species(list(set(map(lambda x: x['patient'], data))))
	return list(map(make_data, data))


def _append_summary(data):
	def make_data(val):
		clients = compose(
			count,
			unique,
			pluck('customer'),
			lambda: val
		)
		animals = compose(
			valmap(count),
			groupby('species'),
			lambda: val
		)
		return {
			'total_val': reduce(lambda total, x: total + x.get('total_vat'), val, 0.00),
			'animals': _get_dict_to_csv(animals()),
			'clients': clients()
		}
	sales_persons = compose(
		valmap(make_data),
		groupby('sales_person_name'),
		lambda: data
	)()

	data.append({'invoice_no': "'-'"})  # for report html (break loop)
	for k, v in sales_persons.items():
		sales_person = k or 'Not specified'
		data.append({'invoice_no': "'Sales Person'", 'item': f"'{sales_person}'"})
		data.append({'invoice_no': "'Total Amt'", 'item': f"'{fmt_money(v.get('total_val'))}'"})
		data.append({'invoice_no': "'Clients'", 'item': f"'{v.get('clients')}'"})
		data.append({'invoice_no': "'Animals'", 'item': f"'{v.get('animals')}'"})
		data.append({})

	return data


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


def _get_dict_to_csv(data, sep=', ', columns=None):
	csv = []
	for k, v in data.items():
		column_name = k or "Others"
		if columns and k in columns:
			column_name = columns[k]
		csv.append(f'{column_name}={v}')
	return sep.join(csv)
