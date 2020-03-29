import frappe
from frappe import _
from toolz import first, compose, pluck, partial

from vet_care.api import get_search_values


def validate(doc, method):
    doc.disabled = doc.vc_deceased
    _validate_patient_activity(doc)
    _set_owner_as_default_customer(doc)
    _validate_default_customer(doc)
    doc.customer = _get_default_customer(doc)
    _set_mobile_no(doc)
    _set_customer_name(doc)


def before_save(doc, method):
    _set_search_values(doc)


def _set_owner_as_default_customer(doc):
    for pet_relation in doc.vc_pet_relation:
        pet_relation.default = (pet_relation.relation == 'Owner')


def _validate_default_customer(doc):
    validate_customer = compose(
        any,
        partial(map, lambda x: x.default)
    )(doc.vc_pet_relation)

    if not validate_customer:
        frappe.throw(_('Please set default customer under Pet Relation'))


def _get_default_customer(doc):
    return compose(
        first,
        partial(map, lambda x: x.customer),
        partial(filter, lambda x: x.default)
    )(doc.vc_pet_relation)


def _set_mobile_no(doc):
    doc.mobile = frappe.get_value('Customer', doc.customer, 'mobile_no')


def _set_customer_name(doc):
    for relation in doc.vc_pet_relation:
        relation.customer_name = frappe.get_value('Customer', relation.customer, 'customer_name')


def _validate_patient_activity(doc):
    if hasattr(doc, '__new_patient_activity') and doc.__new_patient_activity:
        if doc.vc_inpatient:
            description = f'Admitted on {doc.__posting_date} {doc.__posting_time}\n{doc.__reason}'
        else:
            description = f'Dischared on {doc.__posting_date} {doc.__posting_time}\n{doc.__reason}'

        patient_activity = frappe.get_doc({
            'doctype': 'Patient Activity',
            'patient': doc.name,
            'posting_date': doc.__posting_date
        })

        patient_activity.append('items', {
            'activity_type': 'Inpatient',
            'description': description
        })

        patient_activity.save()

        frappe.msgprint(
            f"Inpatient created on Patient Activity {patient_activity.name}"
        )


def _set_search_values(doc):
    if doc.customer:
        doc.vc_search_values = get_search_values(doc.customer)
