import re
import csv


# bench execute vet_care.scripts.scrape.execute --args "['./data/2019.txt', './data/2019_animals.csv']"
def execute(filename, new_filename):
    animals = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.search(r'data2=(\d+)">([- .\/\w]+)</a>', line)
            customer_match = re.search(r'<td class="datarow-odd">([- .\/\w]+)</td>', line)
            customer_match_two = re.search(r'<td class="datarow-even">([- .\/\w]+)</td>', line)
            if match:
                animal_id = match.group(1)
                animal_name = match.group(2)
                customer_name = ''
                if customer_match:
                    customer_name = customer_match.group(1)
                elif customer_match_two:
                    customer_name = customer_match_two.group(1)
                if not _animal_exists(animals, animal_id):
                    animals.append({
                        'id': animal_id,
                        'name': animal_name,
                        'customer_name': customer_name
                    })

    with open(new_filename, 'w') as newfile:
        writer = csv.DictWriter(newfile, fieldnames=['id', 'name', 'customer_name'])
        writer.writeheader()
        for animal in animals:
            writer.writerow(animal)


def _animal_exists(animals, id):
    existing = list(filter(lambda x: x['id'] == id, animals))
    if existing:
        return True
    return False
