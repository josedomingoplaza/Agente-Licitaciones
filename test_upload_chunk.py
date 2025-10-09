"""
Test script that uses the milvus_db modular client to upload a single test chunk and verify it can be searched.
Run this from inside the app container or after activating your venv with Milvus running.
"""
from embedding.milvus_db.connection import milvus_connection
from embedding.milvus_db.client import MilvusClient
import numpy as np

COLLECTION = "licitations"

# simple deterministic 1024-dim vector generator for test
def dummy_embed(text, dim=1024):
    arr = [ord(c) % 256 for c in text]
    if len(arr) < dim:
        arr += [0] * (dim - len(arr))
    return arr[:dim]

chunk = {
    "embedding": dummy_embed("Prueba de carga de chunk"),
    "text_content": "Prueba de carga de chunk",
    "category": "Test",
    "original_heading": "Test heading",
    "licitation_id": "TEST-001",
    "document_name": "test.pdf"
}

if __name__ == '__main__':
    # ensure milvus connection (will use MILVUS_HOST/MILVUS_PORT from env)
    milvus_connection.connect()

    client = MilvusClient()
    collection = client.create_licitation_collection(COLLECTION)
    print('Collection ready:', collection.name)

    res = client.insert_chunks(COLLECTION, [chunk])
    print('Insert result:', res)

    # run a search using the same vector
    q = chunk['embedding']
    results = client.search(COLLECTION, q, limit=3)
    print('Search results:')
    for hit in results[0]:
        print(f"id={hit.id}, distance={hit.distance}, text={hit.entity.get('text_content')}, licitation={hit.entity.get('licitation_id')}")

    milvus_connection.disconnect()
