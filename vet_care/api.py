import frappe
from frappe.utils import today
from toolz import pluck, partial, compose, first


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
