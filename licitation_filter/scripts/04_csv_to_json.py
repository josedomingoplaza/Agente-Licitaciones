import csv
from licitation_filter.utils.utils import load_json, save_json

CSV_FILE_PATH = 'licitation_filter/UNGM_UNSPSC_21-Oct-2025. - UNSPSC.csv'  # Path to your CSV file

data = {}

with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        data[row[-2]] = row[-1]  # Assuming code is in the second last column and product in the last column
        print(f"Product: {row[-1]}, Code: {row[-2]}")
        print(type(row[-2]))


save_json('licitation_filter/reference/UNGM_UNSPSC_21-Oct-2025.json', data)


