"""Retrieval service using Qdrant embeddings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, PointStruct

from .embeddings import EmbeddingService


@dataclass(slots=True)
class RetrievalConfig:
    collection_name: str = "exoai_corpus"
    top_k: int = 5


class RetrievalService:
    """Provides nearest-neighbour search over embedded corpus."""

    def __init__(
        self,
        client: QdrantClient,
        embedding_service: EmbeddingService,
        config: RetrievalConfig | None = None,
    ) -> None:
        self.client = client
        self.embedding_service = embedding_service
        self.config = config or RetrievalConfig()

    def search(self, query: str, *, filters: Filter | None = None) -> List[dict]:
        vector = self.embedding_service.embed_query(query)
        results = self.client.search(
            collection_name=self.config.collection_name,
            query_vector=vector.tolist(),
            limit=self.config.top_k,
            query_filter=filters,
        )
        documents: list[dict] = []
        for point in results:
            payload = point.payload or {}
            documents.append(
                {
                    "id": point.id,
                    "score": point.score,
                    "text": payload.get("text", ""),
                    "metadata": {k: v for k, v in payload.items() if k != "text"},
                }
            )
        return documents


__all__ = ["RetrievalService", "RetrievalConfig"]
