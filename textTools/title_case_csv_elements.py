import csv

# Convierte los elementos de CSV en Mayúsculas Primera Letra
def title_case_csv_elements(elements):
    return [element.title() for element in elements]

filename = "last_name.csv"

with open(filename, "r", newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    modified_rows = [title_case_csv_elements(row) for row in reader]

with open(filename, "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(modified_rows)
