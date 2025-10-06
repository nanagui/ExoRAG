from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.rag.pipeline import EvidenceGenerator
from app.rag.retriever import RetrievalService


class DummyLLM:
    def __init__(self):
        self.prompts = []

    def invoke(self, prompt):
        self.prompts.append(prompt)
        return SimpleNamespace(content="Answer with citations")


class DummyRetriever(RetrievalService):  # type: ignore[misc]
    def __init__(self):
        pass

    def search(self, query: str):
        return [
            {"text": "Evidence A", "score": 0.9, "metadata": {"source": "paper.md"}},
            {"text": "Evidence B", "score": 0.8, "metadata": {"source": "report.md"}},
        ]


def test_evidence_generator_builds_answer():
    generator = EvidenceGenerator(retriever=DummyRetriever(), llm=DummyLLM())
    result = generator.generate("Is this a planet?")
    assert "Answer" in result["answer"]
    assert len(result["documents"]) == 2
