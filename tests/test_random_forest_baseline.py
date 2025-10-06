from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from app.baselines.random_forest import FEATURE_NAMES, train_random_forest


def test_random_forest_pipeline(tmp_path: Path):
    def write_manifest(path: Path, labels):
        with path.open("w") as fh:
            for idx, label in enumerate(labels):
                flux = tmp_path / f"flux_{path.stem}_{idx}.npy"
                np.save(flux, np.random.rand(50).astype(np.float32))
                fh.write(json.dumps({"flux_path": str(flux), "label": int(label)}) + "\n")

    train_manifest = tmp_path / "train.jsonl"
    val_manifest = tmp_path / "val.jsonl"
    write_manifest(train_manifest, [0, 1, 0])
    write_manifest(val_manifest, [1, 0])

    artifact = tmp_path / "rf.joblib"
    reports = train_random_forest(train_manifest, val_manifest, save_path=artifact)
    assert "train_report" in reports
    assert artifact.exists()
    assert len(FEATURE_NAMES) >= 5
