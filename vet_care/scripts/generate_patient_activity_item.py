import frappe
import csv


# bench execute vet_care.scripts.generate_patient_activity_item.execute --args "['./data/processed_patient_activity.csv', './data/cirrusvet_id.csv', './data/unprocessed_total_master.csv', 1000, 0]"
def execute(filename, history_filename, unprocessed_filename, limit, start):
    patient_activities = {}

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cirrus_animal_id = row.get('cirrus_animal_id')
            posting_date = row.get('posting_date')
            patient_activities[f'{cirrus_animal_id}_{posting_date}'] = row.get('patient_activity')

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

    last_line = 0

    with open(history_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        history_item = 0
        for row in reader:
            if history_item > limit:
                break
            cirrus_animal_id = row.get('cirrus_animal_id')
            visit_date = row.get('visit_date')
            patient_activity = patient_activities.get(f'{cirrus_animal_id}_{visit_date}')
            if last_line >= start:
                if patient_activity:
                    print(f'Generating f{history_item}...')
                    _generate_patient_activity_item(patient_activity, row.get('text'))
                    history_item = history_item + 1
                else:
                    unprocessed_data.append({field: row.get(field) for field in fieldnames})
            last_line = last_line + 1

    print(f'Stopped at line {last_line}')

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
