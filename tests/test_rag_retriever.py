from __future__ import annotations

from unittest.mock import MagicMock

from qdrant_client.models import ScoredPoint

from app.rag.embeddings import EmbeddingConfig, EmbeddingService
from app.rag.retriever import RetrievalService


class DummyEmbeddingService(EmbeddingService):  # type: ignore[misc]
    def __init__(self):
        pass

    def embed_query(self, text: str):
        return [0.1, 0.2, 0.3]


def test_retrieval_service_returns_documents(monkeypatch):
    client = MagicMock()
    client.search.return_value = [
        ScoredPoint(id="doc1", score=0.9, payload={"text": "context", "source": "file.md"}),
        ScoredPoint(id="doc2", score=0.8, payload={"text": "context2", "source": "file2.md"}),
    ]

    retriever = RetrievalService(client=client, embedding_service=DummyEmbeddingService())
    docs = retriever.search("question")
    assert len(docs) == 2
    assert docs[0]["metadata"]["source"] == "file.md"
