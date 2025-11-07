import os
import json
import numpy as np
from licitation_filter.utils.utils import load_json
import matplotlib.pyplot as plt

folder = "licitation_filter/data/complete_licitations/no_registered_codes"


description_lengths = []

for filename in os.listdir(folder):
    if filename.endswith(".json"):
        filepath = os.path.join(folder, filename)
        licitation = load_json(filepath, {})
        description = licitation.get("Descripcion", "")
        if len(description) < 1000:
            description_lengths.append(len(description))


average_length = sum(description_lengths) / len(description_lengths) if description_lengths else 0
print(f"Average length of 'Descripcion': {average_length} characters")
print(f"Standard deviation: {np.std(description_lengths)} characters")
print(f"Max length: {max(description_lengths)} characters")
print(f"Min length: {min(description_lengths)} characters")


# Plot histogram
plt.hist(description_lengths, bins=30, color='blue', alpha=0.7)
plt.title("Histogram of 'Descripcion' Lengths")
plt.xlabel("Length (characters)")
plt.ylabel("Number of Licitations")
plt.grid(axis='y', alpha=0.75)
plt.show()


