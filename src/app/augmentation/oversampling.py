"""Class imbalance handling utilities (SMOTE)."""

from __future__ import annotations

from typing import Any, Iterable, Tuple

import numpy as np
from imblearn.over_sampling import SMOTE


def apply_smote(
    features: np.ndarray,
    labels: np.ndarray,
    *,
    sampling_strategy: str | float | dict[str, int] = "minority",
    random_state: int = 42,
    k_neighbors: int = 5,
    **kwargs: Any,
) -> Tuple[np.ndarray, np.ndarray]:
    """Apply SMOTE to rebalance classes."""

    if features.ndim != 2:
        raise ValueError("Features must be 2D (samples, features)")

    smote = SMOTE(
        sampling_strategy=sampling_strategy,
        random_state=random_state,
        k_neighbors=k_neighbors,
        **kwargs,
    )
    resampled_features, resampled_labels = smote.fit_resample(features, labels)
    return resampled_features, resampled_labels


__all__ = ["apply_smote"]
