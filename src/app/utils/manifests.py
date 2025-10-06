"""Helpers for reading dataset manifests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from app.models.datasets import SampleRecord


def load_manifest(path: str | Path) -> List[SampleRecord]:
    records: list[SampleRecord] = []
    manifest_path = Path(path)
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with manifest_path.open() as fh:
        for line in fh:
            if not line.strip():
                continue
            data = json.loads(line)
            records.append(
                SampleRecord(
                    flux_path=Path(data["flux_path"]),
                    time_path=Path(data.get("time_path", data["flux_path"])),
                    label=int(data["label"]),
                    metadata_path=Path(data["metadata_path"]) if data.get("metadata_path") else None,
                )
            )
    return records


__all__ = ["load_manifest"]
