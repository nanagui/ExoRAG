"""Corpus ingestion utilities for RAG."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(slots=True)
class DocumentEntry:
    doc_id: str
    text: str
    metadata: dict[str, str]


def _hash_content(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _chunk_text(text: str, *, chunk_size: int = 1000, overlap: int = 200) -> Iterable[str]:
    if chunk_size <= 0:
        yield text
        return
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        yield text[start:end]
        if end == text_len:
            break
        start = max(end - overlap, 0)


def load_markdown_corpus(directory: str | Path, *, chunk_size: int = 1000, overlap: int = 200) -> List[DocumentEntry]:
    """Load Markdown and text documents into DocumentEntry chunks."""

    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Corpus directory not found: {directory}")

    entries: list[DocumentEntry] = []
    for path in directory.glob("**/*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        content = path.read_text(encoding="utf-8")
        for idx, chunk in enumerate(_chunk_text(content, chunk_size=chunk_size, overlap=overlap)):
            doc_id = f"{path.stem}-{idx}-{_hash_content(chunk)[:8]}"
            entries.append(
                DocumentEntry(
                    doc_id=doc_id,
                    text=chunk,
                    metadata={"source": str(path), "chunk_index": str(idx)},
                )
            )
    return entries


__all__ = ["DocumentEntry", "load_markdown_corpus"]
