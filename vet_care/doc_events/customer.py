import frappe
from frappe import _
from toolz import pluck

from vet_care.doc_events.patient import get_search_values


def validate(doc, method):
    _validate_cpr_as_numeric(doc)


def on_update(doc, method):
    _update_patient_search_values(doc)


def _validate_cpr_as_numeric(doc):
    cpr = doc.vc_cpr
    if cpr and not cpr.isnumeric():
        frappe.throw(_("CPR should be numeric"))


def _update_patient_search_values(doc):
    for patient in pluck(
        "name", frappe.get_all("Patient", filters={"customer": doc.name})
    ):
        frappe.db.set_value(
            "Patient", patient, "vc_search_values", get_search_values(doc.name)
        )
