from __future__ import annotations

import os
from typing import List, Optional, Sequence

from dotenv import load_dotenv
load_dotenv()

try:
    import cohere
    from cohere.errors import NotFoundError
except Exception:
    cohere = None
    NotFoundError = Exception

import numpy as np
from embedding.chunker import Chunk


class CohereEmbedder:
    def __init__(self, model: Optional[str] = None):
        self.model = model or os.environ.get("COHERE_EMBED_MODEL") or "embed-v4.0"
        self.api_key = os.environ.get("COHERE_TRIAL_API_KEY")
        self.client = None
        self.dimension = 1536
        if cohere is not None and self.api_key:
            try:
                self.client = cohere.Client(self.api_key)
            except Exception:
                self.client = None
        print(f"Initialized CohereEmbedder with model: {self.model}")

    def _embed_texts(self, texts: Sequence[str]) -> List[List[float]]:
        if self.client is None:
            print("Could not connect to cohere")
            return [self._fallback_embedding(t) for t in texts]

        try:
            resp = self.client.embed(model=self.model, texts=list(texts))
            print(f"Using model: {self.model}")
            return [list(map(float, vec)) for vec in resp.embeddings]
        except NotFoundError:
            try:
                print("using fallback model embed-english-v2.0")
                fallback_model = "embed-english-v2.0"
                resp = self.client.embed(model=fallback_model, texts=list(texts))
                self.model = fallback_model
                return [list(map(float, vec)) for vec in resp.embeddings]
            except Exception:
                return [self._fallback_embedding(t) for t in texts]
        except Exception:
            return [self._fallback_embedding(t) for t in texts]
        
    def embed_text(self, text: str, dim: Optional[int] = None) -> List[float]:
        if dim is None:
            dim = self.dimension
        vecs = self._embed_texts([text])
        vec = np.array(vecs[0], dtype=np.float32)
        if len(vec) < dim:
            vec = np.concatenate([vec, np.zeros(dim - len(vec), dtype=np.float32)])
        else:
            vec = vec[:dim]
        return vec.tolist()

    @staticmethod
    def _fallback_embedding(text: str, dim: int = 1536) -> List[float]:
        arr = [ord(c) % 256 for c in text]
        if len(arr) < dim:
            arr += [0] * (dim - len(arr))
        return [float(x) for x in arr[:dim]]

    def embed_chunk(self, chunk: Chunk, dim: Optional[int] = None) -> Chunk:
        vecs = self._embed_texts([chunk.content])
        vec = np.array(vecs[0], dtype=np.float32)
        if dim is not None:
            if len(vec) < dim:
                vec = np.concatenate([vec, np.zeros(dim - len(vec), dtype=np.float32)])
            else:
                vec = vec[:dim]
        chunk.embedding = vec.tolist()
        return chunk

    def embed_chunks(self, chunks: Sequence[Chunk], dim: Optional[int] = None) -> List[Chunk]:
        texts = [c.content for c in chunks]
        vecs = self._embed_texts(texts)
        out: List[Chunk] = []
        for c, v in zip(chunks, vecs):
            arr = np.array(v, dtype=np.float32)
            if dim is not None:
                if len(arr) < dim:
                    arr = np.concatenate([arr, np.zeros(dim - len(arr), dtype=np.float32)])
                else:
                    arr = arr[:dim]
            c.embedding = arr.tolist()
            out.append(c)
        return out


if __name__ == "__main__":

    embedder = CohereEmbedder()
    text = "This is a dog"

    embedded_text = embedder.embed_text(text)

    print(f"type(embedded_text): {type(embedded_text)}")
    print(f"len(embedded_text): {len(embedded_text)}")
    print(f"embedded_text[:10]: {embedded_text[:10]}")
