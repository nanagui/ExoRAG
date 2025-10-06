"""Dependency providers for FastAPI routes."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import Depends, HTTPException, status
from qdrant_client import QdrantClient

from .config import get_settings
from .rag.embeddings import EmbeddingService, EmbeddingConfig
from .rag.indexer import QdrantConfig, QdrantIndexer
from .rag.pipeline import EvidenceGenerator
from .rag.retriever import RetrievalConfig, RetrievalService
from .rag.corpus import load_markdown_corpus
from .services.inference import InferenceService, InferenceConfig
from .data.ingestion import LightCurveIngestionService
from .llm_provider import get_llm


@lru_cache(maxsize=1)
def get_inference_service() -> InferenceService:
    settings = get_settings()
    return InferenceService(
        InferenceConfig(
            checkpoint_path=settings.model_checkpoint_path,
            device=None,
        )
    )


@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:
    settings = get_settings()
    if settings.qdrant_url:
        return QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    return QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port, api_key=settings.qdrant_api_key)


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService(EmbeddingConfig())


@lru_cache(maxsize=1)
def get_retrieval_service() -> RetrievalService:
    client = get_qdrant_client()
    embeddings = get_embedding_service()
    settings = get_settings()
    retriever = RetrievalService(
        client=client,
        embedding_service=embeddings,
        config=RetrievalConfig(collection_name=settings.rag_collection_name),
    )
    return retriever


@lru_cache(maxsize=1)
def get_evidence_generator(retriever: RetrievalService | None = None) -> EvidenceGenerator:
    retriever = retriever or get_retrieval_service()
    llm = get_llm()  # Use configured LLM provider
    return EvidenceGenerator(retriever=retriever, llm=llm)


def ensure_corpus_indexed():  # pragma: no cover - executed during app startup
    settings = get_settings()
    if not settings.rag_corpus_dir:
        return
    corpus_dir = Path(settings.rag_corpus_dir)
    if not corpus_dir.exists():
        return
    entries = load_markdown_corpus(corpus_dir)
    if not entries:
        return
    embeddings_service = get_embedding_service()
    vectors = embeddings_service.embed_documents(entry.text for entry in entries)
    client = get_qdrant_client()
    settings = get_settings()
    indexer = QdrantIndexer(client, QdrantConfig(collection_name=settings.rag_collection_name))
    indexer.ensure_collection(vector_size=vectors.shape[1])
    indexer.upsert_documents(entries, vectors)


async def inference_dependency() -> InferenceService:
    try:
        return get_inference_service()
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))


async def retrieval_dependency() -> RetrievalService:
    try:
        return get_retrieval_service()
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))


async def evidence_dependency(
    retriever: RetrievalService = Depends(retrieval_dependency),
) -> EvidenceGenerator:
    try:
        return get_evidence_generator(retriever)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))


def get_ingestion_queue():
    from .workers import SCHEDULER
    return SCHEDULER.ingestion_queue


@lru_cache(maxsize=1)
def get_ingestion_service() -> LightCurveIngestionService:
    return LightCurveIngestionService()
