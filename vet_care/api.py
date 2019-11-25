import frappe

from toolz import pluck, partial, compose


@frappe.whitelist()
def get_pet_relations(pet):
    return compose(list, partial(pluck, 'customer'))(
        frappe.get_all(
            'Pet Relation',
            filters={'parent': pet},
            fields=['customer']
        )
    )
