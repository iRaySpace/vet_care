import frappe
import csv


def execute(filename, history_filename, unprocessed_filename):
    patient_activities = {}

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cirrus_animal_id = row.get('cirrus_animal_id')
            visit_date = row.get('visit_date')
            patient_activities[f'{cirrus_animal_id}_{visit_date}'] = row.get('patient_activity')

    unprocessed_data = []
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

    with open(history_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cirrus_animal_id = row.get('cirrus_animal_id')
            visit_date = row.get('visit_date')
            patient_activity = patient_activities.get(f'{cirrus_animal_id}_{visit_date}')
            if patient_activity:
                _generate_patient_activity_item(patient_activity, row.get('text'))
            else:
                unprocessed_data.append({field: row.get(field) for field in fieldnames})

    with open(unprocessed_filename, 'w') as unprocessed_csvfile:
        writer = csv.DictWriter(unprocessed_csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in unprocessed_data:
            writer.writerow(row)


def _generate_patient_activity_item(parent, description):
    patient_activity = frappe.get_doc('Patient Activity', parent)
    patient_activity.append('items', {
        'activity_type': '',
        'description': description
    })
    patient_activity.save()


def test():
    _generate_patient_activity_item('PA-2020-00009', 'test')
