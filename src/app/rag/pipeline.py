"""Evidence generation pipeline using retrieval + language model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel

from .retriever import RetrievalService


_DEFAULT_PROMPT = """You are an astronomy research assistant. Using the provided context, explain whether the observed signal is a likely exoplanet transit. Cite mission data or papers when available.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer in two concise paragraphs, followed by a bullet list of citations (source paths)."""


@dataclass(slots=True)
class EvidenceConfig:
    prompt_template: str = _DEFAULT_PROMPT


class EvidenceGenerator:
    """Coordinates retrieval and response generation for explanations."""

    def __init__(
        self,
        retriever: RetrievalService,
        llm: BaseLanguageModel,
        config: EvidenceConfig | None = None,
    ) -> None:
        self.retriever = retriever
        self.llm = llm
        self.config = config or EvidenceConfig()
        self.prompt = PromptTemplate(input_variables=["context", "question"], template=self.config.prompt_template)

    def _build_context(self, query: str) -> tuple[str, List[dict[str, Any]]]:
        results = self.retriever.search(query)
        context_chunks = []
        documents: List[dict[str, Any]] = []
        for item in results:
            metadata = item.get("metadata", {})
            documents.append({"text": item.get("text", ""), "metadata": metadata, "score": item.get("score")})
            source = metadata.get("source", "")
            context_chunks.append(f"Source: {source}\nScore: {item.get('score', 0):.3f}\n{item.get('text', '')}")
        return "\n\n".join(context_chunks), documents

    def generate(self, question: str) -> dict[str, Any]:
        context, documents = self._build_context(question)
        prompt_value = self.prompt.format(context=context, question=question)
        if hasattr(self.llm, "invoke"):
            response = self.llm.invoke(prompt_value)
            answer = getattr(response, "content", response)
        else:  # pragma: no cover - fallback
            answer = self.llm(prompt_value)
        return {
            "question": question,
            "answer": answer,
            "documents": documents,
        }


__all__ = ["EvidenceGenerator", "EvidenceConfig"]
