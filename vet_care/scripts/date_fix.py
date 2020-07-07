import csv
import datetime


def execute(filename):
    fields = []
    rows = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        fields = reader.fieldnames
        for row in reader:
            rows.append({
                'cirrus_animal_id': row.get('cirrus_animal_id'),
                'posting_date': _fix_date(row.get('posting_date')),
                'patient_activity': row.get('patient_activity')
            })

    with open(f'final_{filename}', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _fix_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
