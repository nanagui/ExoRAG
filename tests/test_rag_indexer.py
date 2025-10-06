from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
from qdrant_client.models import Distance

from app.rag.corpus import DocumentEntry
from app.rag.indexer import QdrantConfig, QdrantIndexer


def test_indexer_creates_collection_when_missing():
    client = MagicMock()
    client.collection_exists.return_value = False
    indexer = QdrantIndexer(client, QdrantConfig(collection_name="test", distance=Distance.COSINE))
    indexer.ensure_collection(vector_size=10)
    client.create_collection.assert_called_once()


def test_indexer_upsert_points():
    client = MagicMock()
    indexer = QdrantIndexer(client, QdrantConfig(collection_name="test"))
    entries = [DocumentEntry(doc_id="1", text="hello", metadata={}), DocumentEntry(doc_id="2", text="world", metadata={})]
    vectors = np.ones((2, 3), dtype=np.float32)
    indexer.upsert_documents(entries, vectors)
    client.upsert.assert_called_once()
    args, kwargs = client.upsert.call_args
    assert kwargs["collection_name"] == "test"
    assert len(kwargs["points"]) == 2
