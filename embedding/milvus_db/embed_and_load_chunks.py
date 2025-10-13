from pymilvus import Collection
from embedding.chunker import Chunk, Chunker, STANDARD_CATEGORIES
from embedding.cohere_embedder import CohereEmbedder
from embedding.milvus_db.connection import milvus_connection
from embedding.milvus_db.client import MilvusClient
import numpy as np

COLLECTION = "licitations"

embedder = CohereEmbedder()
chunker = Chunker(categories=STANDARD_CATEGORIES)
milvus_connection.connect()
client = MilvusClient()

pdf_file = "embedding/company_licitations/aguas_andinas.pdf"
    
generated_chunks = chunker.generate_chunks(
    pdf_path=pdf_file,
    licitation_id="GS-TBL-2024-01",
    document_name="Bases Especiales TBL"
)

embedded_chunks = []
for chunk in generated_chunks:
    print(f"Embedding: {chunk.heading}")
    chunk = embedder.embed_chunk(chunk, dim=1024)
    embedded_chunks.append(chunk)
    print(f"Successfully embedding {chunk.heading}")

collection = client.create_licitation_collection(COLLECTION)
print('Collection ready:', collection.name)

# Prepare payload matching the schema ordering used by MilvusClient.insert_chunks
chunks_payload = []
for c in embedded_chunks:
    chunks_payload.append({
        "embedding": c.embedding,
        "text_content": c.content,
        "category": c.category or "",
        "original_heading": c.heading or "",
        "licitation_id": c.licitation_id or "",
        "document_name": c.document_name or "",
    })

res = client.insert_chunks(COLLECTION, chunks_payload)
print('Insert result:', res)

inserted_ids = []
try:
    if hasattr(res, "primary_keys"):
        inserted_ids = [int(x) for x in res.primary_keys]
    elif isinstance(res, dict) and "primary_keys" in res:
        inserted_ids = [int(x) for x in res["primary_keys"]]
except Exception:
    inserted_ids = []

while True:
    # col = Collection(COLLECTION)
    # BATCH = 200
    # for i in range(0, len(inserted_ids), BATCH):
    #     batch_ids = inserted_ids[i : i + BATCH]
    #     expr = f"id in [{','.join(map(str, batch_ids))}]"   # NOTE: use [ ... ]
    #     rows = col.query(expr, output_fields=["text_content", "category", "licitation_id", "document_name"])
    #     print(f"Queried {len(rows)} rows for ids {batch_ids[:3]}...")
    #     for r in rows[:5]:
    #         print(r)

    # Semantic search prompt
    print("\nSemantic search: Enter a query to find relevant chunks.")
    query_text = input("Enter your search query: ").strip()
    if query_text:
        query_vec = embedder.embed_text(query_text, dim=1024)
        results = client.search(COLLECTION, query_vec, limit=5)
        print(results[0][0])
        print(type(results))
        # print("\nTop semantic search results:")
        # for idx, hit in enumerate(results):
        #     print(f"Result {idx+1}:")
        #     print(hit)
        #     print("---")
# else:
#     print("No primary keys returned; performing fallback vector search for the first embedded chunk.")
#     qvec = embedded_chunks[0].embedding
#     hits = client.search(COLLECTION, qvec, limit=3)
#     print("Fallback search hits:", hits)