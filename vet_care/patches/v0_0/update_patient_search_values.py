from __future__ import unicode_literals
import frappe
from toolz import pluck

from vet_care.api import get_search_values


def execute():
    fieldname = "vc_search_values"
    for name, customer in frappe.get_all(
        "Patient",
        filters={"customer": ("is", "set")},
        fields=["name", "customer"],
        as_list=1,
    ):
        if customer:
            frappe.db.set_value(
                "Patient", name, fieldname, get_search_values(customer),
            )
