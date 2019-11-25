import frappe

from frappe import _


def validate(doc, method):

    pet = doc.patient
    customer = doc.customer

    if not _is_pet_related_to(pet, customer):
        frappe.throw(_('Pet is not related to the customer'))


def _is_pet_related_to(pet, customer):
    filters = {'parent': pet, 'customer': customer}
    pet_relations = frappe.get_all('Pet Relation', filters=filters)
    return len(pet_relations) > 0
