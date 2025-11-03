import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedding.cohere_embedder import CohereEmbedder
import cohere
import time
import os
import json
from licitation_filter.utils.utils import load_json, save_json

products_es = [
    # Servicios principales
    "Ingeniería",
    "Construcción",
    "Obras Civiles",
    "EPC",
    "Agua Potable",
    "Zanjeo",
    "Sistemas de Agua",

    # Industrias clave
    "Minería",
    "Energía",
    "Acero",
    "Cemento",
    "Agua",

    # Servicios técnicos específicos
    "Instrumentación",
    "Telemetría",
    "SCADA",
    "Especificaciones Técnicas",

    # Servicios de consultoría y gestión
    "Consultoría",
    "Gestión de Proyectos",
    "Estudios de Factibilidad",
    "Estudios de Alcance",
    "Análisis de Riesgos",
    "Revisión de Pares",
    "Adquisiciones"
]

file_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
embeddings_path = os.path.join(file_root, "reference", "product_embeddings_es.json")
unregistered_codes_path = os.path.join(file_root, "data", "unregistered_codes", "25102025_unregistered_codes.json")

embedder = CohereEmbedder()

# embeddings = {}

# for product in products_es:
#     print(f"Embedding product: {product}")
#     embedding = embedder.embed_text(product)
#     embeddings[product] = embedding
    
# save_json(embeddings_path, embeddings)


"""embeddings = load_json(embeddings_path, {})
unregistered_codes = load_json(unregistered_codes_path, {})
scores = {}

for code, product in unregistered_codes.items():
    print(f"Processing code: {code}, product: {product}")
    product_embedding = embedder.embed_text(product)

    score_per_term = []

    for term, term_embedding in embeddings.items():
        sim = cosine_similarity(
            np.array(product_embedding).reshape(1, -1),
            np.array(term_embedding).reshape(1, -1)
        )[0][0]
        score_per_term.append(sim)

    product_score = sum(score_per_term) / len(score_per_term)
    scores[code] = {
        "product": product,
        "scores": score_per_term,
        "average_score": product_score
    }

save_json(os.path.join(file_root, "data", "25102025_unregistered_codes_scored.json"), scores)"""

test_text = "Ingeniería"

test_embedding = embedder.embed_text(test_text)
embeddings = load_json(embeddings_path, {})
score_per_term = []
for term, term_embedding in embeddings.items():
    sim = cosine_similarity(
        np.array(test_embedding).reshape(1, -1),
        np.array(term_embedding).reshape(1, -1)
    )[0][0]
    score_per_term.append(sim)

score = sum(score_per_term) / len(score_per_term)
print(f"Score for '{test_text}': {score}")
