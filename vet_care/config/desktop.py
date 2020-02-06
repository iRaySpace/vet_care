# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _


def get_data():
	return [
		{
			"module_name": "Vet Care",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Vet Care")
		},
		{
			"module_name": "Animal Overview",
			"color": "#7578F6",
			"icon": "fa fa-list-alt",
			"type": "list",
			"label": _("Animal Overview"),
			"_doctype": "Animal Overview"
		},
		{
			"module_name": "Patient Booking",
			"color": "#FF888B",
			"icon": "fa fa-calendar-plus-o",
			"type": "list",
			"label": _("Patient Booking"),
			"_doctype": "Patient Booking"
		}
	]
