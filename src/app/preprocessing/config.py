"""Configuration structures for preprocessing pipelines."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PreprocessingConfig:
    window_length: int = 401
    sigma: float = 5.0
    normalize: bool = True
    phase_fold: bool = True
    period: float | None = None
    period_min: float | None = None
    period_max: float | None = None
    mask_outliers: bool = True

