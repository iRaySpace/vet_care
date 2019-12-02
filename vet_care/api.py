import frappe

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
