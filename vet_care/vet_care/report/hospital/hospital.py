# Copyright (c) 2013, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils.data import today, date_diff

from toolz import compose, partial

# TODO: add owner


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_columns(filters):
	def make_column(label, fieldname, width, fieldtype='Data', options=''):
		return {
			'label': _(label),
			'fieldname': fieldname,
			'fieldtype': fieldtype,
			'width': width,
			'options': options
		}

	return [
		make_column('Species', 'species', 100, 'Link', 'Species'),
		make_column('Animal', 'animal', 100, 'Link', 'Patient'),
		make_column('Owner', 'owner', 150, 'Link', 'Customer'),
		make_column('Date Admitted', 'date_admitted', 130),
		make_column('Days', 'days', 80)
	]


def get_data(filters):
	compute_data = partial(_compute_days, today())
	return compose(list, partial(map, compute_data))(_get_inpatient_records(filters))


def _get_inpatient_records(filters):
	return frappe.db.sql("""
		SELECT
			vc_species AS species,
			customer AS owner,
			patient AS animal,
			DATE(admitted_datetime) AS date_admitted
		FROM `tabInpatient Record`
		INNER JOIN `tabPatient` ON `tabInpatient Record`.patient = `tabPatient`.name
	""", as_dict=1)


def _compute_days(latest_date, record):
	print(record)
	record_with_day = record
	record_with_day['days'] = date_diff(latest_date, record['date_admitted'])
	return record_with_day
