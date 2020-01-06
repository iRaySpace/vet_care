import frappe
import json
from frappe.utils import today
from toolz import pluck, partial, compose, first, concat


@frappe.whitelist()
def get_pet_relations(pet):
    return compose(list, partial(pluck, 'customer'))(
        frappe.get_all(
            'Pet Relation',
            filters={'parent': pet},
            fields=['customer']
        )
    )


@frappe.whitelist()
def apply_core_overrides():
    frappe.db.sql("""
        UPDATE `tabDocField` 
        SET set_only_once = 0
        WHERE parent = 'Patient'
        AND fieldname = 'customer'
    """)
    frappe.db.sql("""
        UPDATE `tabDocType`
        SET autoname = 'VS-.#####'
        WHERE name = 'Vital Signs'
    """)
    frappe.db.commit()

    return True


@frappe.whitelist()
def make_invoice(dt, dn):
    sales_invoice = frappe.new_doc('Sales Invoice')

    template = frappe.get_value('Lab Test', dn, 'template')
    rate = frappe.get_value('Lab Test Template', template, 'lab_test_rate')

    sales_invoice.append('items', {
        'item_code': template,
        'qty': 1,
        'rate': rate,
        'reference_dt': dt,
        'reference_dn': dn
    })

    patient = frappe.get_value('Lab Test', dn, 'patient')
    customer = frappe.get_value('Patient', patient, 'customer')
    sales_invoice.update({
        'patient': patient,
        'customer': customer,
        'due_date': today()
    })

    sales_invoice.set_missing_values()

    return sales_invoice


@frappe.whitelist()
def make_invoice_for_encounter(dt, dn):
    sales_invoice = frappe.new_doc('Sales Invoice')

    practitioner = frappe.get_value('Patient Encounter', dn, 'practitioner')
    op_consulting_charge_item = frappe.get_value('Healthcare Practitioner', practitioner, 'op_consulting_charge_item')
    op_consulting_charge = frappe.db.get_value('Healthcare Practitioner', practitioner, 'op_consulting_charge')

    sales_invoice.append('items', {
        'item_code': op_consulting_charge_item,
        'qty': 1,
        'rate': op_consulting_charge,
        'reference_dt': dt,
        'reference_dn': dn
    })

    patient = frappe.get_value('Patient Encounter', dn, 'patient')
    customer = frappe.get_value('Patient', patient, 'customer')

    sales_invoice.update({
        'patient': patient,
        'customer': customer,
        'due_date': today()
    })

    sales_invoice.set_missing_values()

    return sales_invoice


# deprecated
@frappe.whitelist()
def get_medical_records(patient):
    return frappe.get_all(
        'Patient Medical Record',
        filters={'patient': patient},
        fields=['reference_doctype', 'reference_name', 'communication_date']
    )


@frappe.whitelist()
def close_invoice(items, patient, customer):
    items = json.loads(items)

    sales_invoice = frappe.new_doc('Sales Invoice')
    sales_invoice.update({
        'patient': patient,
        'customer': customer,
        'due_date': today()
    })

    for item in items:
        sales_invoice.append('items', {
            'item_code': item.get('item_code'),
            'qty': item.get('qty'),
            'rate': item.get('rate')
        })

    sales_invoice.set_missing_values()
    sales_invoice.submit()

    return sales_invoice


@frappe.whitelist()
def get_clinical_history(patient, filter_length):
    """
    Patient's Clinical History is consist of:
    (1) Patient Activity
    (2) Sales Invoice Items

    Clinical History returns structurally:
    ('posting_date', 'description', 'price')
    """
    def patient_activity_mapper(patient_activity):
        return {
            'posting_date': patient_activity.get('posting_date'),
            'description': f"{patient_activity.get('activity_type').upper()}: {patient_activity.get('description')}",
            'price': ''
        }

    def sales_invoice_item_mapper(sales_invoice_item):
        return {
            'posting_date': sales_invoice_item.get('posting_date'),
            'description': f"{sales_invoice_item.get('qty')} x {sales_invoice_item.get('item_code')}",
            'price': sales_invoice_item.get('amount')
        }

    get_patient_activities = compose(
        list,
        partial(map, patient_activity_mapper)
    )

    get_sales_invoice_items = compose(
        list,
        partial(map, sales_invoice_item_mapper)
    )

    print(filter_length)

    return list(concat([
        get_patient_activities(
            frappe.get_all(
                'Patient Activity',
                filters={'patient': patient},
                fields=['posting_date', 'activity_type', 'description']
            )
        ),
        get_sales_invoice_items(
            _get_sales_invoice_items(frappe.get_value('Patient', patient, 'customer'))
        )
    ]))


@frappe.whitelist()
def make_patient_activity(patient, activity_type, description):
    patient_activity = frappe.get_doc({
        'doctype': 'Patient Activity',
        'patient': patient,
        'posting_date': today(),
        'activity_type': activity_type,
        'description': description
    })
    patient_activity.save()

    return patient_activity


def _get_sales_invoice_items(customer):
    return frappe.db.sql("""
        SELECT 
            si.posting_date,
            si_item.item_code,
            si_item.qty,
            si_item.amount
        FROM `tabSales Invoice Item` si_item
        INNER JOIN `tabSales Invoice` si ON si.name = si_item.parent
        WHERE si.customer = %s
    """, (customer,), as_dict=1)
