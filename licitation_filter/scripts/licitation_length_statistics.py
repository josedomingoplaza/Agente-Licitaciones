import os
from pathlib import Path
import numpy as np
import config
from licitation_filter.utils.utils import load_json
import matplotlib.pyplot as plt

passed_licitations_directory = config.PROJECT_ROOT / "licitation_filter" / "data" / "complete_licitations" / "passed_filter"

description_lengths = []

for filename in os.listdir(passed_licitations_directory):
    if filename.endswith(".json"):
        filepath = os.path.join(passed_licitations_directory, filename)
        licitation = load_json(filepath, {})
        description = licitation.get("Descripcion", "")
        if len(description) < 1000:
            description_lengths.append(len(description))


average_length = sum(description_lengths) / len(description_lengths) if description_lengths else 0
print(f"Average length of 'Descripcion': {average_length} characters")
print(f"Standard deviation: {np.std(description_lengths)} characters")
print(f"Max length: {max(description_lengths)} characters")
print(f"Min length: {min(description_lengths)} characters")

plt.hist(description_lengths, bins=30, color='blue', alpha=0.7)
plt.title("Histogram of 'Descripcion' Lengths")
plt.xlabel("Length (characters)")
plt.ylabel("Number of Licitations")
plt.grid(axis='y', alpha=0.75)
plt.show()


