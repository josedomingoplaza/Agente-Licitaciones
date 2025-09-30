import re
import ollama
from pypdf import PdfReader
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Chunk:
    """Represents a chunk of text with its metadata."""
    heading: str
    content: str
    category: Optional[str] = None
    licitation_id: Optional[str] = None
    document_name: Optional[str] = None

class Chunker:
    """
    A class for processing PDF documents into structured, categorized chunks.
    Handles both structural chunking (based on headings) and semantic classification.
    """
    
    def __init__(self, 
        categories: List[str], 
        model_name: str = 'llama3:8b',
        heading_pattern: str = r"(^\d+(\.\d+)*\s+[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s/]+$)"):
      
        self.chunk_categories = categories
        self.model_name = model_name
        self.heading_pattern = heading_pattern
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        full_pdf_text = ""
        for page in reader.pages:
            full_pdf_text += page.extract_text() + "\n"
        return full_pdf_text
    
    def _create_dumb_chunks(self, document_text: str) -> List[Chunk]:
        pattern = self.heading_pattern
        parts = re.split(pattern, document_text, flags=re.MULTILINE)
        
        chunks = []
        
        if len(parts) > 0 and parts[0].strip():
            chunks.append(Chunk(
                heading="Introducción",
                content=parts[0].strip()
            ))
        
        for i in range(1, len(parts), 3):
            if i < len(parts):
                heading = parts[i].strip()
                content = parts[i + 2].strip() if (i + 2) < len(parts) else ""
                
                if heading and content:
                    chunks.append(Chunk(
                        heading=heading,
                        content=content
                    ))
        
        return chunks
    
    def _classify_chunk(self, chunk: Chunk) -> str:
        
        prompt = f"""
            You are an expert analyst. Your task is to categorize a section from a licitation document.
            Based on the text provided, classify it into the single most appropriate category from the following list.
            Your response must be ONLY ONE of the category names.

            Eres un analista experto. Tu tarea es categorizar una sección de una licitación.
            Clasifica el texto dado en una de las siguientes categorías de la lista a continuación
            Tu respuesta debe ser SOLAMENTE UNA de las categorías.  

            Categorías: {', '.join(self.chunk_categories)}

            Texto a clasificar:
            ---
            {chunk.heading}
            {chunk.content[:2000]}
            ---

            Responde solamente con el nombre de la categoría
            """
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            category = response['message']['content'].strip()
            
            # Validate that the returned category is in our list
            if category in self.chunk_categories:
                return category
            else:
                # Return closest match or default
                return self._find_closest_category(category)
                
        except Exception as e:
            print(f"Error classifying chunk: {e}")
            return "Administrative & General Information"  # Default category
    
    def _find_closest_category(self, returned_category: str) -> str:
        returned_lower = returned_category.lower()
        for category in self.chunk_categories:
            if any(word in category.lower() for word in returned_lower.split()):
                return category
        return self.chunk_categories[0]  # Return first category as fallback
    
    def pdf_to_chunks(self, 
                   pdf_path: str, 
                   licitation_id: Optional[str] = None,
                   document_name: Optional[str] = None) -> List[Chunk]:

        document_text = self.extract_text_from_pdf(pdf_path)
        
        chunks = self._create_dumb_chunks(document_text)
        
        for chunk in chunks:
            chunk.category = self._classify_chunk(chunk)
            chunk.licitation_id = licitation_id
            chunk.document_name = document_name or pdf_path.split('/')[-1]
        
        return chunks
    
    
    def export_chunks_to_dict(self, chunks: List[Chunk]) -> List[Dict]:
        return [
            {
                'heading': chunk.heading,
                'content': chunk.content,
                'category': chunk.category,
                'licitation_id': chunk.licitation_id,
                'document_name': chunk.document_name
            }
            for chunk in chunks
        ]


# Example usage and configuration
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

    # Process a single PDF
    chunks = chunker.pdf_to_chunks(
        pdf_path="embedding/company_licitations/aguas_andinas.pdf",
        licitation_id="AA-2024-001",
        document_name="Aguas Andinas Contract"
    )

    # Print results
    for i, chunk in enumerate(chunks):
        print(f"--- CHUNK {i+1}: {chunk.heading} ---")
        print(f"Category: {chunk.category}")
        print(f"Content: {chunk.content[:200]}...")
        print("\n")
    print(chunks[3])