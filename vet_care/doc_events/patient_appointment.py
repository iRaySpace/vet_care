import frappe


def validate(doc, method):
    customer = frappe.db.get_value('Patient', doc.patient, 'customer')
    doc.vc_owner = customer
