import frappe


def validate(vital_signs, method):
    vital_signs.bmi = (vital_signs.weight / (vital_signs.height * vital_signs.height))


def on_submit(vital_signs, method):
    patient_activity = frappe.new_doc('Patient Activity')
    patient_activity.update({
        'patient': vital_signs.patient,
        'posting_date': vital_signs.signs_date,
    })
    patient_activity.append('items', {
        'activity_type': 'Vital Signs',
        'description': _get_description(vital_signs),
        'reference_dt': 'Vital Signs',
        'reference_dn': vital_signs.name
    })
    patient_activity.save()
    patient_activity.submit()


def _get_description(vital_signs):
    fields = [
        'temperature:Temperature',
        'pulse:Pulse',
        'respiratory_rate:Respiratory rate',
        'vc_mucous_membrane:Mucous membrane',
        'vc_capillary_refill_time:CRT',
        'vital_signs_note:Note',
        'height:Height',
        'weight:Weight',
        'bmi:BMI'
    ]

    def get_data(field):
        key, label = field.split(':')
        return f'{label}: {vital_signs.get(key)}'

    return '\n'.join(map(get_data, fields))
