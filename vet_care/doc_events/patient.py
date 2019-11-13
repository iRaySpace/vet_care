import frappe


def validate(doc, method):
    doc.disabled = doc.vc_deceased
