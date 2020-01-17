import frappe
import csv
from toolz import first


def execute(filename, unprocessed_filename):
    with open(unprocessed_filename, 'w') as unprocessed_csvfile:
        fieldnames = [
            'cirrus_cm_id',
            'cirrus_animal_id',
            'erpnext_cm_id',
            'erpnext_animal_id',
            'animal_name',
            'gender',
            'species',
            'breed',
            'weight_kgs',
            'visit_date',
            'text'
        ]
        writer = csv.DictWriter(unprocessed_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                patients = _get_patients(row.get('animal_name'), row.get('erpnext_cm_id'))
                if len(patients) == 1:
                    patient = first(patients)
                    _set_cirrusvet_id(patient.get('name'), row.get('cirrus_animal_id'))
                else:
                    writer.writerow({field: row.get(field) for field in fieldnames})


def _set_cirrusvet_id(name, cirrusvet_id):
    frappe.db.set_value('Patient', name, 'vc_cirrusvet', cirrusvet_id)


def _get_patients(patient_name, customer):
    return frappe.get_all(
        'Patient',
        filters={
            'patient_name': patient_name,
            'customer': customer
        }
    )


def test():
    patients = _get_patients('Animal 2', 'Customer 2')
    if len(patients) == 1:
        patient = first(patients)
        print(patient)
