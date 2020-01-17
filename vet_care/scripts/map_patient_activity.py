import frappe
import csv


def execute(filename):
    patient_activities = frappe.get_all('Patient Activity', fields=['name', 'patient', 'posting_date'])
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['cirrus_animal_id', 'posting_date', 'patient_activity'])
        writer.writeheader()
        for row in patient_activities:
            cirrus_animal_id = frappe.db.get_value('Patient', row.get('patient'), 'vc_cirrusvet')
            posting_date = row.get('posting_date')
            writer.writerow({
                'cirrus_animal_id': cirrus_animal_id,
                'posting_date': posting_date.strftime("%d-%m-%Y"),
                'patient_activity': row.get('name')
            })


def test():
    posting_date = frappe.db.get_value('Patient Activity', 'PA-2020-00009', 'posting_date')
    print(posting_date.strftime("%d-%m-%Y"))
