from __future__ import unicode_literals
import frappe
from toolz import pluck

from vet_care.api import get_search_values


def execute():
    fieldname = "vc_search_values"
    if not frappe.db.exists("Custom Field", f"Customer-{fieldname}"):
        frappe.get_doc(
            {
                "doctype": "Custom Field",
                "dt": "Customer",
                "label": "Phone, CPR etc.",
                "fieldname": fieldname,
                "fieldtype": "Small Text",
                "insert_after": "customer_details",
                "in_standard_filter": 1,
                "hidden": 1,
            }
        ).insert()
    for (name,) in frappe.get_all(
        "Customer", filters={fieldname: ("is", "not set")}, fields=["name"], as_list=1,
    ):
        frappe.db.set_value(
            "Customer", name, fieldname, get_search_values(name),
        )
