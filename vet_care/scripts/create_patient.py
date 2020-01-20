import frappe
import csv

animals = []


# bench execute vet_care.scripts.create_patient.execute --args "['./new_patients.csv']"
def execute(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f'Importing {row.get("vc_cirrusvet")}...')
            patient = frappe.new_doc('Patient')
            patient.update({
                'patient_name': row.get('patient_name'),
                'sex': row.get('sex'),
                'vc_weight': row.get('vc_weight'),
                'vc_species': row.get('vc_species'),
                'vc_breed': row.get('vc_breed'),
                'vc_cirrusvet': row.get('vc_cirrusvet')
            })
            patient.append('vc_pet_relation', {
                'default': 1,
                'relation': 'Owner',
                'customer': row.get('customer')
            })
            patient.save()

