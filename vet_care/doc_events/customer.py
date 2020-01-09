import frappe
from frappe import _


def validate(doc, method):
    _validate_cpr_as_numeric(doc)


def _validate_cpr_as_numeric(doc):
    cpr = doc.vc_cpr
    if cpr and not cpr.isnumeric():
        frappe.throw(_('CPR should be numeric'))
