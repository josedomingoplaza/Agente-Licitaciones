# Example: Splitting chunk content into sentences using spaCy
import spacy

# Load the Spanish spaCy model (make sure to install it first: python -m spacy download es_core_news_sm)
nlp = spacy.load("es_core_news_sm")

def split_chunk_into_sentences(chunk_content):
    doc = nlp(chunk_content)
    return [sent.text.strip() for sent in doc.sents]

# Example usage
chunk_text = """
El proyecto debe completarse en seis meses. Los participantes deben presentar garantías. La evaluación será técnica y financiera.
"""

sentences = split_chunk_into_sentences(chunk_text)
for i, sentence in enumerate(sentences):
    print(f"Sentence {i+1}: {sentence}")