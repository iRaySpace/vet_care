import frappe
from frappe.utils import today
from random import shuffle


def load_dummy_patient_activity(length, patient):
    print(f"Loading {length} dummy Patient Activity to {patient}...")

    ten_words = ['the', 'of', 'and', 'which', 'each', 'she', 'do', 'how', 'their', 'if']
    activity_types = ['History', 'Examination', 'Notes', 'Plan']

    for x in range(length):
        shuffle(ten_words)
        shuffle(activity_types)

        patient_activity = frappe.get_doc({
            'doctype': 'Patient Activity',
            'patient': patient,
            'posting_date': today(),
            'activity_type': activity_types[0],
            'description': ' '.join(ten_words[:3])
        })

        patient_activity.save()

