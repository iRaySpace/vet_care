# -*- coding: utf-8 -*-
# Copyright (c) 2019, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class VetcareSettings(Document):
	def validate(self):
		_check_pos_bahrain()


def _check_pos_bahrain():
	pos_bahrain = frappe.get_all(
		'Module Def',
		filters={'name': 'Pos Bahrain'}
	)
	if not pos_bahrain:
		frappe.throw(_('Please install POS Bahrain app'))
