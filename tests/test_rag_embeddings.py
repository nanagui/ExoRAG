from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest

import app.rag.embeddings as embeddings_module
from app.rag.embeddings import EmbeddingService


class DummyModel:
    def __init__(self, *args, **kwargs):
        self.encode_calls = []

    def encode(self, texts, batch_size=32, normalize_embeddings=True):
        self.encode_calls.append(list(texts))
        return np.ones((len(texts), 3))


@pytest.fixture(autouse=True)
def patch_sentence_transformer(monkeypatch):
    monkeypatch.setattr(embeddings_module, "SentenceTransformer", DummyModel)
    yield
    monkeypatch.setattr(embeddings_module, "SentenceTransformer", DummyModel)


def test_embedding_service_embeddings():
    service = EmbeddingService()
    docs = ["one", "two"]
    vectors = service.embed_documents(docs)
    assert vectors.shape == (2, 3)
    query = service.embed_query("hello")
    assert query.shape == (3,)
