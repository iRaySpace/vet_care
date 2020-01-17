import csv


def execute(filename):
    patient_activities = {}

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            visit_date = row.get('visit_date')
            cirrus_animal_id = row.get('cirrus_animal_id')
            existing_patient_activities = patient_activities.get(visit_date)
            if not existing_patient_activities:
                patient_activities[visit_date] = [cirrus_animal_id]
            else:
                if cirrus_animal_id not in existing_patient_activities:
                    existing_patient_activities.append(cirrus_animal_id)

    with open(f'processed_{filename}', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['cirrus_animal_id', 'visit_date'])
        writer.writeheader()
        for visit_date in patient_activities.keys():
            for animal_id in patient_activities.get(visit_date):
                writer.writerow({
                    'cirrus_animal_id': animal_id,
                    'visit_date': visit_date
                })
