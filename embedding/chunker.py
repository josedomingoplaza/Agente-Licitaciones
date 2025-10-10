import re
from typing import List, Dict, Optional
from dataclasses import dataclass

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

import ollama
from docling.document_converter import DocumentConverter

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

@dataclass
class Chunk:
    heading: str
    content: str
    category: Optional[str] = None
    licitation_id: Optional[str] = None
    document_name: Optional[str] = None
    embedding: Optional[List[float]] = None

class Chunker:
    def __init__(self, 
        categories: List[str], 
        model_name: str = 'llama3:8b'):
      
        self.chunk_categories = categories
        self.model_name = model_name
        self.converter = DocumentConverter()
        self.embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.category_embeddings = self.embedder.encode(self.chunk_categories, convert_to_numpy=True)

    
    def pdf_to_markdown(self, pdf_path: str) -> str:
        try:
            result = self.converter.convert(pdf_path)
            document = result.document
            return document.export_to_markdown()
        except Exception as e:
            print(f"Error converting PDF to Markdown: {e}")
            return "" 
    
    def _parse_markdown(self, markdown_text: str) -> List[Chunk]:
        lines = markdown_text.split('\n')
        chunks = []
        current_content = []
        current_heading = "" 

        for line in lines:
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                if current_content:
                    chunks.append(Chunk(
                        heading=current_heading,
                        content="\n".join(current_content).strip()
                    ))
                
                current_heading = match.group(2).strip()
                current_content = []
            else:
                if line.strip(): 
                    current_content.append(line)

        if current_content:
            chunks.append(Chunk(
                heading=current_heading,
                content="\n".join(current_content).strip()
            ))
        
        return chunks
    
    def _classify_chunk(self, chunk: Chunk) -> str:
        prompt = f"""
            Eres un analista experto. Tu tarea es categorizar una sección de un documento de licitación.
            Basándote en el texto proporcionado (incluyendo el encabezado), clasifícalo en la única categoría más apropiada.
            Tu respuesta debe ser SOLAMENTE UNA de las categorías de la lista.

            Categorías: {', '.join(self.chunk_categories)}

            Texto a clasificar:
            ---
            Encabezado: {chunk.heading}

            Contenido:
            {chunk.content[:2000]}
            ---

            Categoría:
            """
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            category = response['message']['content'].strip()
            
            if category in self.chunk_categories:
                return category
            else:
                return self._find_closest_category(category)
                
        except Exception as e:
            print(f"Error during chunk classification: {e}")
            return "Información Administrativa y General"

    def _find_closest_category(self, returned_category: str) -> str:
        try:
            input_embedding = self.embedder.encode([returned_category], convert_to_numpy=True)
            scores = cosine_similarity(input_embedding, self.category_embeddings)[0]
            best_idx = int(np.argmax(scores))
            return self.chunk_categories[best_idx]
        except Exception as e:
            print(f"Error in semantic category matching: {e}")
            return self.chunk_categories[-1]
    
    def generate_chunks(self, 
        pdf_path: str, 
        licitation_id: Optional[str] = None,
        document_name: Optional[str] = None) -> List[Chunk]:

        print(f"1. Converting '{pdf_path}' to Markdown...")
        markdown_text = self.pdf_to_markdown(pdf_path)
        if not markdown_text:
            return []

        print("2. Parsing Markdown into structural chunks...")
        chunks = self._parse_markdown(markdown_text)
        
        print(f"3. Classifying {len(chunks)} chunks...")
        for i, chunk in enumerate(chunks):
            print(f"   - Classifying chunk {i+1}/{len(chunks)} ('{chunk.heading[:50]}...')")
            chunk.category = self._classify_chunk(chunk)
            chunk.licitation_id = licitation_id
            chunk.document_name = document_name or pdf_path.split('/')[-1]
        
        print("4. Chunk generation complete.")
        return chunks
    
    def export_chunks_to_dict(self, chunks: List[Chunk]) -> List[Dict]:
        return [chunk.__dict__ for chunk in chunks]

if __name__ == "__main__":
    
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

    # Print the results for verification
    print("\n--- RESULTS ---")
    for i, chunk in enumerate(generated_chunks):
        print(f"\n--- CHUNK {i+1} ---")
        print(f"Licitacion ID: {chunk.licitation_id}")
        print(f"Heading: {chunk.heading}")
        print(f"Assigned Category: {chunk.category}")
        print(f"Content Preview: {chunk.content[:250].strip()}...")