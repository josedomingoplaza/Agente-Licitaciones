import config

import re
from typing import List, Dict, Optional
from dataclasses import dataclass

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

import ollama
from docling.document_converter import DocumentConverter

import spacy

from openai import OpenAI
import dotenv
import os
from pathlib import Path
dotenv.load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

STANDARD_CATEGORIES = [
        "Alcance del Proyecto y Requisitos Técnicos",
        "Información Financiera y Presupuestaria",
        "Cláusulas Legales y Términos Contractuales",
        "Plazos y Cronograma del Proyecto",
        "Garantías y Fianzas Requeridas",
        "Requisitos y Documentos de los Participantes",
        "Criterios de Evaluación",
        "Información Administrativa y General",
        "Texto muy sucio para ser categorizado"
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
        self.ollama_client = ollama.Client(host="http://ollama:11434")
        self.nlp = spacy.load("es_core_news_sm")
        self.openai_client = OpenAI()

    def pdf_to_markdown(self, pdf_path: str) -> str:
        try:
            result = self.converter.convert(pdf_path)
            document = result.document
            return document.export_to_markdown()
        except Exception as e:
            print(f"Error converting PDF to Markdown: {e}")
            return ""
        
    def clean_document(self, text: str) -> str:
        clean_text = text.replace("<!-- image -->", "").strip()
        clean_text = clean_text.replace("-", "")
        return clean_text

    def split_into_sentences(self, text: str) -> list[str]:
        doc = self.nlp(text.replace("\n", " "))
        return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    def normalize_whitespace(self, text: str) -> str:
        text = re.sub(r'[ \t]+', ' ', text)
        text = '\n'.join(line.strip() for line in text.splitlines())
        text = re.sub(r'\n{2,}', '\n\n', text)
        return text.strip()

    def _handle_large_chunk(self, current_heading: str, content_str: str, max_chunk_length: int = 1000) -> List[Chunk]:
        sentences = self.split_into_sentences(content_str)
        chunks = []
        temp_content = []

        for sentence in sentences:
            if len(" ".join(temp_content + [sentence])) <= max_chunk_length:
                temp_content.append(sentence)
            else:
                if temp_content:
                    temp_content_str = ' '.join(temp_content)
                    temp_content_str = self.normalize_whitespace(temp_content_str)
                    chunks.append(
                        Chunk(
                            heading=current_heading,
                            content=f"{current_heading}\n{temp_content_str.strip()}"
                        )
                    )
                temp_content = [sentence]

        if temp_content:
            temp_content_str = ' '.join(temp_content)
            temp_content_str = self.normalize_whitespace(temp_content_str)
            chunks.append(
                Chunk(
                    heading=current_heading,
                    content=f"{current_heading}\n{temp_content_str.strip()}"
                )
            )

        return chunks
    
    def _remove_index(self, markdown_text: str, scan_lines: int = 100) -> str:
        lines = markdown_text.splitlines()
        cleaned: List[str] = []
        limit = min(scan_lines, len(lines))

        for i, ln in enumerate(lines):
            if i < limit:
                if ln.count('.') > 3:
                    continue
                if ln.count('|') >= 2:
                    continue
            cleaned.append(ln)

        return "\n".join(cleaned)

    def _parse_markdown(self, markdown_text: str, max_chunk_length: int = 1000) -> List[Chunk]:
        markdown_text = self._remove_index(markdown_text)
        markdown_text = self.clean_document(markdown_text)
        lines = markdown_text.split('\n')
        chunks = []
        current_content = []
        current_heading = ""

        for line in lines:
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                if current_content:
                    content_str = "\n".join(current_content).strip()
                    content_str = f"{current_heading}\n{content_str}".strip()
                    if len(content_str) > max_chunk_length:
                        chunks.extend(self._handle_large_chunk(current_heading, content_str, max_chunk_length))
                    else:
                        chunks.append(Chunk(heading=current_heading, content=content_str))
                current_heading = match.group(2).strip()
                current_content = []
            elif line.strip():
                current_content.append(line)

        if current_content:
            content_str = "\n".join(current_content).strip()
            if len(content_str) > max_chunk_length:
                chunks.extend(self._handle_large_chunk(current_heading, content_str, max_chunk_length))
            else:
                chunks.append(Chunk(heading=current_heading, content=content_str))

        return chunks
    
    def _classify_chunk(self, chunk: Chunk) -> str:
        instructions = """Eres un analista experto. Tu tarea es categorizar una sección de un documento de licitación.
            Basándote en el texto proporcionado (incluyendo el encabezado), clasifícalo en la única categoría más apropiada.
            Tu respuesta debe ser SOLAMENTE UNA de las categorías de la lista."""
        
        prompt = f"""
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
            response = self.openai_client.responses.create(
                model="gpt-5-nano-2025-08-07",  
                instructions= instructions, 
                input=prompt,                
            )
            category = response.output_text.strip()
            
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
        return {i: chunk.__dict__ for i, chunk in enumerate(chunks)}

   