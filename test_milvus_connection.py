
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import numpy as np

# Simple embedding function: mean of char codes, padded/truncated to dim=8
def embed_text(text, dim=8):
    arr = [ord(c) for c in text]
    if len(arr) < dim:
        arr += [0] * (dim - len(arr))
    return np.array(arr[:dim], dtype=np.float32)

# 1. Connect to Milvus
connections.connect("default", host="milvus", port="19530")

# 2. Define collection schema with an additional "licitation" field
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=8),
    FieldSchema(name="licitation", dtype=DataType.VARCHAR, max_length=128),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=256),
]
schema = CollectionSchema(fields, description="Test collection with licitation")

# 3. Create collection
collection_name = "test_chunks"
if collection_name in utility.list_collections():
    Collection(collection_name).drop()
collection = Collection(name=collection_name, schema=schema)

# 4. Embed and insert 3 sentences
sentences = [
    "Milvus is a vector database.",
    "This project analyzes licitations.",
    "Embeddings are useful for search."
]
embeddings = [embed_text(s).tolist() for s in sentences]
licitations = [f"licit_{i}" for i in range(3)]
insert_result = collection.insert([embeddings, licitations, sentences])

# 5. Create index and load collection
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 8}
}
collection.create_index(field_name="embedding", index_params=index_params)
collection.load()

# 6. Interactive search loop
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("Type a sentence to search for the most similar chunk (Ctrl+C to exit):")
while True:
    try:
        user_text = input("Query: ")
        user_emb = embed_text(user_text).tolist()
        results = collection.search(
            data=[user_emb],
            anns_field="embedding",
            param={"metric_type": "L2", "params": {"nprobe": 8}},
            limit=1,
            output_fields=["licitation", "text"]
        )
        hit = results[0][0]
        # For demonstration, also print cosine similarity
        entity = collection.query(expr=f"id == {hit.id}", output_fields=["embedding"])[0]
        db_emb = entity["embedding"]
        sim = cosine_similarity(user_emb, db_emb)
        print(f"Most similar: Text=\"{hit.entity.get('text')}\", Licitation={hit.entity.get('licitation')}, Distance={hit.distance:.4f}, Cosine similarity={sim:.4f}")
    except KeyboardInterrupt:
        print("\nExiting.")
        break