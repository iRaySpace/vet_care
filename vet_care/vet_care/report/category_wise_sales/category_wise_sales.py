# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from functools import reduce


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
		make_column('Item Group', 'item_group', 130, 'Link', 'Item Group'),
		make_column('Gross Sales', 'gross_sales', 130, 'Currency'),
	]


def _get_data(filters):
	def make_data(row, data):
		item_group = data.get('item_group')
		if item_group not in row:
			row[item_group] = 0.0
		row[item_group] = row[item_group] + data.get('amount')
		return row

	si_data = frappe.db.sql("""
		SELECT
			sii.item_code,
			sii.amount
		FROM `tabSales Invoice Item` sii
		INNER JOIN `tabSales Invoice` si
		ON sii.parent = si.name
		WHERE si.docstatus = 1
		AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
	""", filters, as_dict=True)

	item_groups = _get_item_groups(si_data)
	grouped_data = list(
		map(lambda x: {
			'item_group': item_groups[x.get('item_code')],
			'amount': x.get('amount')
		}, si_data)
	)

	summed_data = reduce(make_data, grouped_data, {})

	return list(
		map(lambda x: {
			'item_group': x,
			'gross_sales': summed_data[x]
		}, summed_data.keys())
	)


def _get_item_groups(si_data):
	item_groups = {}
	for row in si_data:
		item_code = row.get('item_code')
		if item_code not in item_groups:
			item_group = frappe.get_value('Item', item_code, 'item_group')
			item_groups[item_code] = item_group
	return item_groups
