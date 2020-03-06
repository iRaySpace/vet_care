import csv
import datetime
import frappe


# bench execute vet_care.scripts.generate_from_history.execute --args "['./data/new_history.csv']"
def execute(filename):
    patient_activities = []
    not_created = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            timestamp = int(row.get('Date'))
            cirrusvet_id = row.get('AnimalID')
            description = row.get('Notes')
            date = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
            patient = _get_patient_via_cirrusvet_id(cirrusvet_id)
            if patient:
                patient_activity = _pick_or_new_patient_activity(patient_activities, patient, date)
                patient_activity.append('items', {'description': description})
                patient_activities.append(patient_activity)
            else:
                not_created.append(cirrusvet_id)
        created = 0
        total = len(patient_activities)
        for patient_activity in patient_activities:
            patient_activity.save()
            created = created + 1
            print(f'Created ${created}/${total} patient activities')
    print(not_created)


def _pick_or_new_patient_activity(patient_activities, patient, date):
    def filter_activity(activity):
        return activity.patient == patient and activity.posting_date == date

    existing = list(filter(filter_activity, patient_activities))
    if existing:
        return existing[0]

    return frappe.get_doc({
        'doctype': 'Patient Activity',
        'patient': patient,
        'posting_date': date
    })


def _get_patient_via_cirrusvet_id(cirrusvet_id):
    patient_data = frappe.db.sql(
        """SELECT name FROM `tabPatient` WHERE vc_cirrusvet=%s""",
        cirrusvet_id,
        as_dict=True
    )
    if patient_data:
        return patient_data[0].get('name')
    return None
