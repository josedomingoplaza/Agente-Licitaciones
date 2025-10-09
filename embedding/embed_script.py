from embedding.chunker import Chunk, Chunker
from embedding.cohere_embedder import CohereEmbedder

embedder = CohereEmbedder()

STANDARD_CATEGORIES = [
        "Alcance del Proyecto y Requisitos Técnicos",
        "Información Financiera y Presupuestaria",
        "Cláusulas Legales y Términos Contractuales",
        "Plazos y Cronograma del Proyecto",
        "Garantías y Fianzas Requeridas",
        "Requisitos y Documentos de los Participantes",
        "Criterios de Evaluación",
        "Información Administrativa y General",
    ]
    
chunker = Chunker(categories=STANDARD_CATEGORIES)

pdf_file = "embedding/company_licitations/aguas_andinas.pdf"
    
generated_chunks = chunker.generate_chunks(
    pdf_path=pdf_file,
    licitation_id="GS-TBL-2024-01",
    document_name="Bases Especiales TBL"
)

for chunk in generated_chunks:
    print(f"Chunking: {chunk.heading}")
    chunk = embedder.embed_chunk(chunk)
    print(f"Successfully chunked {chunk.heading}")

# Print the results for verification
print("\n--- RESULTS ---")
for i, chunk in enumerate(generated_chunks):
    print(f"\n--- CHUNK {i+1} ---")
    print(f"Licitacion ID: {chunk.licitation_id}")
    print(f"Heading: {chunk.heading}")
    print(f"Assigned Category: {chunk.category}")
    print(f"Content Preview: {chunk.content[:250].strip()}...")
    print(f"Embedding: {chunk.embedding[:5]}")
    