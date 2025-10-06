"""Qdrant index management."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from .corpus import DocumentEntry


@dataclass(slots=True)
class QdrantConfig:
    collection_name: str = "exoai_corpus"
    vector_size: int | None = None
    distance: Distance = Distance.COSINE
    recreate_collection: bool = False


class QdrantIndexer:
    """Handles collection lifecycle and upsert in Qdrant."""

    def __init__(self, client: QdrantClient, config: QdrantConfig | None = None) -> None:
        self.client = client
        self.config = config or QdrantConfig()

    def ensure_collection(self, vector_size: int) -> None:
        cfg = self.config
        if cfg.recreate_collection:
            self.client.recreate_collection(
                collection_name=cfg.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=cfg.distance),
            )
        else:
            if not self.client.collection_exists(cfg.collection_name):
                self.client.create_collection(
                    collection_name=cfg.collection_name,
                    vectors_config=VectorParams(size=vector_size, distance=cfg.distance),
                )

    def upsert_documents(self, entries: Iterable[DocumentEntry], embeddings: np.ndarray) -> None:
        points = []
        for entry, vector in zip(entries, embeddings):
            points.append(
                PointStruct(
                    id=entry.doc_id,
                    vector=vector.tolist(),
                    payload={"text": entry.text, **entry.metadata},
                )
            )
        if points:
            self.client.upsert(collection_name=self.config.collection_name, points=points)


__all__ = ["QdrantIndexer", "QdrantConfig"]
