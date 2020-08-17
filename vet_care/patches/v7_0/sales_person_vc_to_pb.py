from __future__ import unicode_literals
import frappe
from vet_care.utils import check_pos_bahrain


def execute():
    if check_pos_bahrain():
        sales_invoices = frappe.get_all(
            'Sales Invoice',
            filters={'pb_sales_employee': ''},
            fields=[
                'name',
                'pb_sales_employee',
                'pb_sales_person',
                'pb_sales_person_name'
            ]
        )
        for sales_invoice in sales_invoices:
            pb_sales_person = sales_invoice.get('pb_sales_person')  # vetcare
            pb_sales_employee = sales_invoice.get('pb_sales_employee')  # pos_bahrain
            if pb_sales_person and not pb_sales_employee:
                name = sales_invoice.get('name')
                pb_sales_person_name = sales_invoice.get('pb_sales_person_name')
                frappe.db.set_value('Sales Invoice', name, 'pb_sales_employee', pb_sales_person, update_modified=False)
                frappe.db.set_value('Sales Invoice', name, 'pb_sales_employee_name', pb_sales_person_name, update_modified=False)
