"""Random Forest baseline for quick benchmarking."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Tuple

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


FEATURE_NAMES = [
    "flux_mean",
    "flux_std",
    "flux_min",
    "flux_max",
    "flux_ptp",
    "flux_skew",
    "flux_kurtosis",
]


def _load_flux(path: Path) -> np.ndarray:
    if path.suffix == ".npz":
        data = np.load(path)
        return data["flux"]
    return np.load(path)


def _extract_features(flux: np.ndarray) -> np.ndarray:
    from scipy.stats import kurtosis, skew

    return np.array(
        [
            np.mean(flux),
            np.std(flux),
            np.min(flux),
            np.max(flux),
            np.ptp(flux),
            skew(flux),
            kurtosis(flux),
        ],
        dtype=np.float32,
    )


def _load_manifest(path: Path) -> Tuple[np.ndarray, np.ndarray]:
    xs, ys = [], []
    with path.open() as fh:
        for line in fh:
            if not line.strip():
                continue
            data = json.loads(line)
            flux = _load_flux(Path(data["flux_path"]))
            xs.append(_extract_features(flux))
            ys.append(int(data["label"]))
    return np.stack(xs), np.array(ys)


def train_random_forest(train_manifest: Path, val_manifest: Path | None = None, *, save_path: Path | None = None) -> dict:
    X_train, y_train = _load_manifest(train_manifest)
    model = RandomForestClassifier(n_estimators=300, max_depth=None, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)

    results = {"train_report": classification_report(y_train, model.predict(X_train), output_dict=True)}

    if val_manifest:
        X_val, y_val = _load_manifest(val_manifest)
        results["val_report"] = classification_report(y_val, model.predict(X_val), output_dict=True)

    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": model, "feature_names": FEATURE_NAMES}, save_path)

    return results


__all__ = ["train_random_forest", "FEATURE_NAMES"]
