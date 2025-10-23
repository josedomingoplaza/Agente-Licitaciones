from web_scraping.mercado_publico_client import MercadoPublicoClient, Estado
import time
import matplotlib.pyplot as plt
from collections import Counter
import os
import pandas as pd

# client = MercadoPublicoClient()

# licitations_per_day = []

# for day in range(1, 20):
#     if day < 10:
#         codes = client.get_licitation_codes_for_day(f"0{day}102025", Estado.PUBLICADA)
#     else:
#         codes = client.get_licitation_codes_for_day(f"{day}102025", Estado.PUBLICADA)
#     licitations_per_day.append(len(codes))

#     print(f"Got {len(codes)} codes for day {day}")
#     time.sleep(2)



# print(licitations_per_day)

# print(f"Average licitations per day: {sum(licitations_per_day) / len(licitations_per_day)}")

# plt.plot(licitations_per_day)
# plt.show()


import json

with open("json_references/licitations_10102025.json", "r", encoding="utf-8") as f:
    data = json.load(f)

lics_per_date = {}

for lic in data:
    fecha_creacion = lic.get("Fechas", {}).get("FechaCreacion")
    lics_per_date[fecha_creacion[:10]] = lics_per_date.get(fecha_creacion, 0) + 1


print(lics_per_date)