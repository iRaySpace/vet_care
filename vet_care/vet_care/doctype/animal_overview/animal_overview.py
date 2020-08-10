# -*- coding: utf-8 -*-
# Copyright (c) 2020, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from toolz import compose, first, pluck
from frappe.model.document import Document
from functools import partial


class AnimalOverview(Document):
	def validate(self):
		_set_attach_to_animal(self)


def _set_attach_to_animal(animal_overview):
	if not animal_overview.animal and animal_overview.attach:
		frappe.throw(_('Please set animal field'))
	if not animal_overview.attach:
		return
	file = compose(
		first,
		partial(pluck, 'name'),
	)(
		frappe.get_all(
			'File',
			filters={
				'attached_to_name': 'Animal Overview',
				'attached_to_doctype': 'Animal Overview'
			}
		)
	)
	frappe.db.sql(
		"""
			UPDATE 
				`tabFile`
			SET
				attached_to_name = %(attached_to_name)s,
				attached_to_doctype = 'Patient'
			WHERE
				name = %(name)s
		""",
		{
			'attached_to_name': animal_overview.animal,
			'name': file
		}
	)
	animal_overview.attach = None
