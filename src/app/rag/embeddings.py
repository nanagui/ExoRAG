"""Embedding service for RAG pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import numpy as np

try:  # pragma: no cover - heavy dependency check
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover
    SentenceTransformer = None  # type: ignore


DEFAULT_MODEL_NAME = "BAAI/bge-base-en-v1.5"


@dataclass(slots=True)
class EmbeddingConfig:
    model_name: str = DEFAULT_MODEL_NAME
    device: str | None = None


class EmbeddingService:
    """Wraps SentenceTransformer to embed documents and queries."""

    def __init__(self, config: EmbeddingConfig | None = None) -> None:
        self.config = config or EmbeddingConfig()
        if SentenceTransformer is None:  # pragma: no cover
            raise ImportError("sentence-transformers is not installed")
        self.model = SentenceTransformer(self.config.model_name, device=self.config.device)

    def embed_documents(self, texts: Iterable[str]) -> np.ndarray:
        vectors = self.model.encode(list(texts), batch_size=32, normalize_embeddings=True)
        return np.asarray(vectors, dtype=np.float32)

    def embed_query(self, text: str) -> np.ndarray:
        vector = self.model.encode([text], batch_size=1, normalize_embeddings=True)[0]
        return np.asarray(vector, dtype=np.float32)


__all__ = ["EmbeddingService", "EmbeddingConfig", "DEFAULT_MODEL_NAME"]
