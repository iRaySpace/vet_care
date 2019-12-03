import frappe
from frappe.utils.safe_exec import get_safe_globals as core_get_safe_globals
from frappe.utils.print_format import download_pdf as core_download_pdf
from vet_care.utils import calculate_age


@frappe.whitelist()
def download_pdf(doctype, name, format=None, doc=None, no_letterhead=0):
    frappe.utils.safe_exec.get_safe_globals = get_safe_globals(
        core_get_safe_globals
    )
    core_download_pdf(doctype, name, format, doc, no_letterhead)

# TODO: refactor
def get_safe_globals(func):
    def inner():
        return func().update(
            frappe._dict(
                calculate_age=calculate_age
            )
        )
    return inner
