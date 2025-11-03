import os
import json

folder = "licitation_filter/data/complete_licitaciones/passed_filter"
field_name = "Descripcion"  # Replace with the field you want to extract

tokens = []
licitations_per_day = {}

for filename in os.listdir(folder):
    if filename.endswith(".json"):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            value = data.get(field_name)
            date = data.get("Fechas").get("FechaPublicacion")[:10]
            if date in licitations_per_day.keys():
                licitations_per_day[date] += 1
            else:
                licitations_per_day[date] = 1
            if value:
                tokens.append(len(value)/4)
            else:
                print(f"{field_name} not found in {filename}")

print(f"Average tokens of {field_name}: {sum(tokens) / len(tokens) if tokens else 0}")

print(f"Files in directory: {len(os.listdir(folder))}")

print(licitations_per_day)


