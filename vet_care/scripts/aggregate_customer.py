import csv


# bench execute vet_care.scripts.aggregate_customer.execute --args "['./data/missing_animals.csv', './data/missing_customers.csv']"
def execute(animals, customers):
    existing_customers = {}
    with open(customers, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer = row.get('customer')
            customer_id = row.get('customer_id')
            existing_customers[customer] = customer_id

    new_data = []
    with open(animals, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            new_data.append({
                'id': row.get('id'),
                'name': row.get('name'),
                'customer_name': row.get('customer_name'),
                'customer_id': existing_customers[row.get('customer_name')],
            })

    with open('./data/missing_data.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'name', 'customer_name', 'customer_id'])
        writer.writeheader()
        for row in new_data:
            writer.writerow(row)
