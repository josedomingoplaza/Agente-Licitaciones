import numpy as np
from licitation_filter.utils.utils import load_json


chunks = load_json("embedding/testin_whitespace_remover.json", {})

character_count = []
for key in chunks.keys():
    character_count.append(len(chunks[key].get("content", "")))
    if len(chunks[key].get("content", "")) > 1900:
        print(chunks[key].get("content", ""))
        print(f"Key: {key}")
        print("\n ------ \n")

character_count.sort()
print(character_count)

print(f"Average Character Count: {sum(character_count) / len(character_count) if character_count else 0}")
print(f"Max Character Count: {max(character_count) if character_count else 0}")
print(f"Min Character Count: {min(character_count) if character_count else 0}")
print(f"Standard Deviation of Character Count: {np.std(character_count) if character_count else 0}")
print(f"Median Character Count: {np.median(character_count) if character_count else 0}")

content = "Desempeño\nMatriz EPP (según especialidad)                                                       | Especificación de los EPP relacionados a los trabajos a efectuar. E indicando la normativa a los cuales están suscritos. | |"

import re

def normalize_whitespace(text: str) -> str:
    # Replace multiple spaces/tabs with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove leading/trailing spaces on each line
    text = '\n'.join(line.strip() for line in text.splitlines())
    # Optionally, collapse multiple blank lines to a single blank line
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()

print("\n\n")
print(normalize_whitespace(content))