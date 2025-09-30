import spacy
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

# NEW: Import HuggingFace transformers and sentence-transformers
from sentence_transformers import SentenceTransformer

class ManualSemanticChunker:
    """
    A transparent semantic chunker using a HuggingFace embedding model.
    """
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        print("Initializing HuggingFace SentenceTransformer model...")
        self.embedding_model = SentenceTransformer(model_name)
        self.nlp = spacy.load("es_core_news_sm")
        print("Model initialized.")

    def chunk(self, text: str, similarity_threshold: float, verbose: bool = False):
        """
        Processes a text into semantically cohesive chunks.
        """
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 5]

        if not sentences:
            return []

        # --- HuggingFace SentenceTransformer API ---
        sentence_embeddings = self.embedding_model.encode(sentences)
        # ------------------------------------------

        # Calculate similarity between adjacent sentences
        similarities = [cosine_similarity([sentence_embeddings[i]], [sentence_embeddings[i+1]])[0][0] for i in range(len(sentences)-1)]

        if verbose:
            print("\n--- Similarity between consecutive sentences (using HuggingFace SentenceTransformer) ---")
            for i, score in enumerate(similarities):
                print(f"Similarity between Sentence {i+1} and {i+2}: {score:.4f}")
            print("--------------------------------------------------\n")

        # Group sentences into chunks
        final_chunks = []
        current_chunk_sentences = [sentences[0]]

        for i, similarity in enumerate(similarities):
            if similarity < similarity_threshold:
                final_chunks.append(" ".join(current_chunk_sentences))
                current_chunk_sentences = [sentences[i+1]]
            else:
                current_chunk_sentences.append(sentences[i+1])
        
        if current_chunk_sentences:
            final_chunks.append(" ".join(current_chunk_sentences))

        return final_chunks

# --- Main Execution ---

if __name__ == "__main__":
    sample_text = """
    Para arreglar una motosierra, primero asegúrate de que la cadena esté bien tensada y lubricada. Revisa el filtro de aire y límpialo si está sucio para evitar problemas de encendido. Finalmente, verifica que la bujía funcione correctamente y reemplázala si es necesario.

Había una vez un ratón curioso que vivía en un campo de trigo dorado. Un día encontró una semilla mágica que, al plantarla, creció hasta convertirse en un árbol gigante. Desde entonces, el ratón y sus amigos disfrutaron de la sombra y los frutos del árbol todos los días.

Las personas nacen libres e iguales en dignidad y derechos. La familia es el núcleo fundamental de la sociedad. El Estado reconoce y ampara a los grupos intermedios a través de los cuales se organiza y estructura la sociedad.
Se solicita una empresa especializada en servicios de limpieza para oficinas y espacios comunes. El trabajo incluye la limpieza diaria de pisos, ventanas, baños y áreas de recepción, garantizando altos estándares de higiene. Los interesados deben contar con experiencia comprobable y presentar una propuesta detallada de servicios y costos.

    """

    chunker = ManualSemanticChunker()
    test_threshold = 0.5

    print(f"\n--- Testing with a similarity threshold of: {test_threshold} ---")
    
    final_chunks = chunker.chunk(sample_text, similarity_threshold=test_threshold, verbose=True)

    print(f"Result: Created {len(final_chunks)} chunks.\n")
    for i, chunk in enumerate(final_chunks):
        print(f"--- Chunk {i+1} ---")
        print(chunk)
        print("-" * 20)