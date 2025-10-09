from __future__ import annotations

import os
from typing import List, Optional, Sequence, Union

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
        self.model = model or os.environ.get("COHERE_EMBED_MODEL") or "embed-multilingual-v2"
        self.api_key = os.environ.get("COHERE_TRIAL_API_KEY")
        self.client = None
        if cohere is not None and self.api_key:
            try:
                self.client = cohere.Client(self.api_key)
            except Exception:
                self.client = None

    def _embed_texts(self, texts: Sequence[str]) -> List[List[float]]:
        if self.client is None:
            print("Could not connect to cohere")
            return [self._fallback_embedding(t) for t in texts]

        try:
            resp = self.client.embed(model=self.model, texts=list(texts))
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

    @staticmethod
    def _fallback_embedding(text: str, dim: int = 1024) -> List[float]:
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
    # Quick local test: create a few Spanish chunks and embed them
    samples = [
        Chunk(heading="h1", content="Los perros corren en el parque"),
        Chunk(heading="h2", content="La tubería principal tiene una fuga"),
        Chunk(heading="h3", content="El presupuesto estimado es alto")
    ]

    emb = CohereEmbedder()
    print(f"Using Cohere model: {emb.model}; client present: {emb.client is not None}")
    res = emb.embed_chunks(samples, dim=1024)
    for i, c in enumerate(res, 1):
        print(f"Chunk {i}: heading={c.heading}, emb_len={len(c.embedding) if c.embedding else 0}, first5={c.embedding[:5] if c.embedding else None}")
