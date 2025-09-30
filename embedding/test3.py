import os
from dotenv import load_dotenv

# Import the necessary LangChain components
from langchain_cohere import CohereEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

# --- 1. Load Environment Variables ---
# This line loads the variables from your .env file (e.g., COHERE_TRIAL_API_KEY)
load_dotenv()

# Retrieve the API key from the environment.
# The script will exit if the key is not found.
cohere_api_key = os.getenv("COHERE_TRIAL_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_TRIAL_API_KEY not found in .env file. Please add it.")

# --- 2. The Text to be Chunked ---
# Using the same text with the clear topic shift to "Ancient Rome"
sample_text = """
El adjudicatario será responsable del diseño, suministro e instalación de todos los componentes. Esto incluye tableros eléctricos de baja tensión, canalizaciones, cableado de fuerza y control, y la integración completa con el sistema SCADA existente. El proponente deberá presentar un plan de trabajo detallado en formato de Carta Gantt. Es mandatorio que todos los materiales eléctricos cuenten con certificación de la Superintendencia de Electricidad y Combustibles (SEC).

La garantía por seriedad de la oferta será una boleta bancaria por un valor de $5.000.000 CLP. Dicha garantía debe tener una validez de 90 días desde la fecha de presentación de la oferta. En caso de adjudicación, se deberá entregar una segunda garantía de fiel cumplimiento del contrato, equivalente al 10% del valor total del proyecto. La devolución de las garantías se realizará 30 días después de la recepción final de las obras.

La antigua Roma fue una de las civilizaciones más influyentes de la historia, conocida por su vasto imperio y avances en arquitectura, derecho y gobierno. Sus legiones conquistaron gran parte de Europa, el norte de África y Asia Menor, dejando una huella duradera en la cultura occidental. El Imperio Romano finalmente cayó en el año 476 d.C., marcando el inicio de la Edad Media.
"""

# --- 3. Initialize the Embedding Model and the Chunker ---

# Initialize the powerful Cohere Embedding Model using the loaded API key.
# We specify the multilingual model for the best performance on Spanish text.
print("Initializing Cohere embedding model...")
cohere_embeddings = CohereEmbeddings(
    cohere_api_key=cohere_api_key,
    model="embed-multilingual-v3.0"
)
print("Model initialized.")

# Initialize LangChain's SemanticChunker, passing in the Cohere embeddings.
# The chunker will now use Cohere to understand the semantics of the sentences.
text_splitter = SemanticChunker(cohere_embeddings)


# --- 4. Create and Print the Chunks ---
print("\n--- Running LangChain's SemanticChunker powered by Cohere ---")

# The .create_documents() method runs the entire process.
docs = text_splitter.create_documents([sample_text])

print(f"\nResult: Successfully created {len(docs)} chunks.\n")
for i, doc in enumerate(docs):
    print(f"--- Chunk {i+1} ---")
    print(doc.page_content)
    print("-" * 20)