# -*- coding: utf-8 -*-
# Copyright (c) 2019, 9T9IT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
from vet_care.utils import check_pos_bahrain


class VetcareSettings(Document):
	def validate(self):
		check_pos_bahrain(True)
