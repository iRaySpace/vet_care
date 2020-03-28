from __future__ import unicode_literals
import frappe
from toolz import pluck

from vet_care.api import get_search_values


def execute():
    fieldname = "vc_search_values"
    if not frappe.db.exists("Custom Field", f"Patient-{fieldname}"):
        frappe.get_doc(
            {
                "doctype": "Custom Field",
                "dt": "Patient",
                "label": "Search Values",
                "fieldname": fieldname,
                "fieldtype": "Small Text",
                "insert_after": "customer",
                "in_standard_filter": 1,
                "hidden": 1,
            }
        ).insert()
    for name, customer in frappe.get_all(
        "Patient",
        filters={fieldname: ("is", "not set"), "customer": ("is", "set")},
        fields=["name", "customer"],
        as_list=1,
    ):
        if customer:
            frappe.db.set_value(
                "Patient", name, fieldname, get_search_values(customer),
            )
