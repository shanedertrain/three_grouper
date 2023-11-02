import csv
import random
from pathlib import Path
from datetime import datetime
from itertools import cycle

PATH_INPUT_FOLDER = Path(__file__).parent / Path('input') 
PATH_OUTPUT_FOLDER = Path(__file__).parent / Path('output') 
PATH_PEOPLE = PATH_INPUT_FOLDER / 'people.csv'

VERBOSE = True

ELDER = 'Elder'
JOURNEYMAN = 'Journeyman'
APPRENTICE = 'Apprentice'

# Define a class to represent people
class Person:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def __str__(self):
        return f"Name: {self.name}, Category: {self.category}"

# Function to create a template CSV file if it doesn't exist
def create_template_csv():
    with open(PATH_PEOPLE, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Category'])
        writer.writerow(['Person1', ELDER])
        writer.writerow(['Person2', ELDER])
        writer.writerow(['Person3', ELDER])
        writer.writerow(['Person4', JOURNEYMAN])
        writer.writerow(['Person5', JOURNEYMAN])
        writer.writerow(['Person6', JOURNEYMAN])
        writer.writerow(['Person7', JOURNEYMAN])
        writer.writerow(['Person8', APPRENTICE])
        writer.writerow(['Person9', APPRENTICE])
        writer.writerow(['Person10', APPRENTICE])
        writer.writerow(['Person11', APPRENTICE])

# Function to read the CSV file and return a list of dictionaries
def read_people_csv():
    people_list = []
    with open(PATH_PEOPLE, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            person = Person(row['Name'], row['Category'])
            people_list.append(person)
    return people_list

def print_groups(groups:list[list[Person]]):
    for i, group in enumerate(groups):
        print(f"Group {i+1}: {[f'{person.name, person.category}' for person in group]}")
    print("")

# Function to sort people into groups based on the given conditions
def sort_people_into_groups(people_list: list[Person]) -> list[list[Person]]:
    groups: list[list[Person]] = []
    shuffled_people_list = people_list.copy()  # Create a copy of the original list
    random.shuffle(shuffled_people_list)  # Shuffle the people list to ensure random selection

    # Make groups using elders
    for person in shuffled_people_list:
        if person.category == ELDER:
            groups.append([person])
            people_list.remove(person)  # Remove the person from the original list

    if VERBOSE: print_groups(groups)

    # Make groups using apprentice, journeymen. prioritize for one of each here.
    for group in groups:
        shuffled_people_list = people_list.copy()
        random.shuffle(shuffled_people_list)  # Shuffle the people list to ensure random selection
        for person in shuffled_people_list:
            categories_in_group = [person.category for person in group]
            if person.category == APPRENTICE and APPRENTICE not in categories_in_group:
                group.append(person)
                people_list.remove(person)  # Remove the person from the original list
            elif person.category == JOURNEYMAN and JOURNEYMAN not in categories_in_group:
                group.append(person)
                people_list.remove(person)  # Remove the person from the original list

            if len(group) == 3:
                break

    if VERBOSE: print_groups(groups)

    if VERBOSE: print(f"Remaining: {[f'{person.name, person.category}' for person in people_list]}")

    return groups

# Function to fill remaining slots in groups with available people
def fill_remaining_slots(groups: list[list[Person]], people_list: list[Person]) -> list[list[Person]]:
    group_cycle = cycle(groups)
    for person in people_list:
        current_group = next(group_cycle)
        current_group.append(person)
    return groups

# Function to write the sorted groups into a file in CSV format
def write_groups_to_file(groups: list[list[Person]]):
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = PATH_OUTPUT_FOLDER / f"sorted_groups_{current_datetime}.txt"
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Category'])
        writer.writerow([])
        for i, group in enumerate(groups, start=1):
            writer.writerow([f"Group {i}:", ''])
            for person in group:
                writer.writerow([person.name, person.category])
            writer.writerow([])  # Add an empty row for separation between groups

def main():
    # Check if the people.csv file exists, if not, create a template
    if not PATH_PEOPLE.exists():
        create_template_csv()

    # Read the CSV file
    people_list = read_people_csv()

    # Sort people into groups based on the given conditions
    groups = sort_people_into_groups(people_list)

    # Fill the remaining slots in groups with available people
    groups = fill_remaining_slots(groups, people_list)

    # Print the final groups
    print_groups(groups)

    # Write the sorted groups to a file, dated in YYYY-MM-DD format
    write_groups_to_file(groups)

if __name__ == "__main__":
    main()