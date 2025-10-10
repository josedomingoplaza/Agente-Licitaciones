from embedding.chunker import Chunk, Chunker, STANDARD_CATEGORIES
from embedding.cohere_embedder import CohereEmbedder

embedder = CohereEmbedder()
    
chunker = Chunker(categories=STANDARD_CATEGORIES)

pdf_file = "embedding/company_licitations/aguas_andinas.pdf"
    
generated_chunks = chunker.generate_chunks(
    pdf_path=pdf_file,
    licitation_id="GS-TBL-2024-01",
    document_name="Bases Especiales TBL"
)

# for chunk in generated_chunks:
#     print(f"Chunking: {chunk.heading}")
#     chunk = embedder.embed_chunk(chunk)
#     print(f"Successfully chunked {chunk.heading}")

print(f"{embedder.embed_chunk(generated_chunks[0]).heading}: {embedder.embed_chunk(generated_chunks[0]).embedding[:20]}")


    