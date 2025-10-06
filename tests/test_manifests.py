from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from app.utils.manifests import load_manifest


def test_load_manifest_reads_json_lines(tmp_path: Path):
    manifest = tmp_path / "train.jsonl"
    flux = tmp_path / "flux.npy"
    np.save(flux, np.ones(5))
    entries = [
        {"flux_path": str(flux), "time_path": str(flux), "label": 1, "metadata_path": None},
        {"flux_path": str(flux), "label": 0},
    ]
    with manifest.open("w") as fh:
        for entry in entries:
            fh.write(json.dumps(entry) + "\n")
    records = load_manifest(manifest)
    assert len(records) == 2
    assert records[0].label == 1
    assert records[1].time_path == Path(flux)


def test_load_manifest_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_manifest(tmp_path / "missing.jsonl")
