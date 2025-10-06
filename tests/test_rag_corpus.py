from __future__ import annotations

from pathlib import Path

from app.rag.corpus import DocumentEntry, load_markdown_corpus


def test_load_markdown_corpus_chunks(tmp_path: Path):
    file_path = tmp_path / "doc.md"
    file_path.write_text("A" * 50 + "\n" + "B" * 50)

    entries = load_markdown_corpus(tmp_path, chunk_size=40, overlap=10)
    assert len(entries) >= 3
    assert all(isinstance(entry, DocumentEntry) for entry in entries)


def test_load_markdown_corpus_missing(tmp_path: Path):
    missing = tmp_path / "none"
    missing.mkdir()
    (missing / "ignore.json").write_text("{}")
    # Should not raise for empty directory
    entries = load_markdown_corpus(missing)
    assert entries == []
