from pymilvus import Collection
from embedding.chunker import Chunker, STANDARD_CATEGORIES
from embedding.cohere_embedder import CohereEmbedder
from embedding.milvus_db.connection import milvus_connection
from embedding.milvus_db.client import MilvusClient
import numpy as np
import os

COLLECTION = "licitations"
PDF_FOLDER = "embedding/buffer"

embedder = CohereEmbedder()
chunker = Chunker(categories=STANDARD_CATEGORIES)
milvus_connection.connect()
client = MilvusClient()

# Create collection if not exists
collection = client.create_licitation_collection(COLLECTION)
print('Collection ready:', collection.name)

# Iterate through all PDFs in the folder
doc_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]
all_chunks = []
for pdf_file in doc_files:
    pdf_path = os.path.join(PDF_FOLDER, pdf_file)
    print(f"Processing: {pdf_file}")
    licitation_id = os.path.splitext(pdf_file)[0]
    document_name = pdf_file
    try:
        generated_chunks = chunker.generate_chunks(
            pdf_path=pdf_path,
            licitation_id=licitation_id,
            document_name=document_name
        )
        print(f"Sample chunk content: {generated_chunks[0].content[:30]}...")
        embedded_chunks = embedder.embed_chunks(generated_chunks, dim=1024)
        all_chunks.extend(embedded_chunks)
        print(f"Embedded {len(embedded_chunks)} chunks from {pdf_file}")
    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")

# Prepare payload for Milvus
chunks_payload = []
for c in all_chunks:
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

# Semantic search loop
while True:
    print("\nSemantic search: Enter a query to find relevant chunks.")
    query_text = input("Enter your search query: ").strip()
    if query_text:
        query_vec = embedder.embed_text(query_text, dim=1024)
        results = client.search(COLLECTION, query_vec, limit=5)
        print("\nTop semantic search results:")
        for idx, hit in enumerate(results[0] if isinstance(results[0], list) else results):
            print(f"Result {idx+1}:")
            print(hit)
            print("---")
