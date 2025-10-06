"""End-to-end preprocessing pipeline for light curves."""

from __future__ import annotations

import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from .config import PreprocessingConfig
from .validation import validate_preprocessed_output

try:  # pragma: no cover - optional heavy dependency
    import lightkurve as lk
except ImportError:  # pragma: no cover
    lk = None  # type: ignore

LOGGER = logging.getLogger(__name__)


class PreprocessingError(RuntimeError):
    """Raised when preprocessing fails."""


def _ensure_lightkurve() -> None:
    if lk is None:  # pragma: no cover
        raise ImportError(
            "lightkurve library is required for preprocessing. Install dependencies first."
        )


def _load_lightcurve(path: Path, flux_column: str) -> "lk.LightCurve":  # type: ignore[name-defined]
    _ensure_lightkurve()
    try:
        lc = lk.read(path)
        if hasattr(lc, "to_lightcurve"):
            lc = lc.to_lightcurve(flux_column=flux_column)
        return lc
    except Exception as exc:  # pragma: no cover - lightkurve handles many IO errors
        raise PreprocessingError(f"Failed to load light curve: {path}") from exc


def _apply_cleaning(
    lc: "lk.LightCurve", config: PreprocessingConfig
) -> "lk.LightCurve":  # type: ignore[name-defined]
    cleaned = lc
    if config.mask_outliers and hasattr(cleaned, "remove_outliers"):
        cleaned = cleaned.remove_outliers(sigma=config.sigma)
    if hasattr(cleaned, "remove_nans"):
        cleaned = cleaned.remove_nans()
    if hasattr(cleaned, "flatten"):
        cleaned = cleaned.flatten(window_length=config.window_length)
    if config.normalize and hasattr(cleaned, "normalize"):
        cleaned = cleaned.normalize()
    return cleaned


def _phase_fold(
    lc: "lk.LightCurve", config: PreprocessingConfig
) -> "lk.LightCurve":  # type: ignore[name-defined]
    if not config.phase_fold:
        return lc
    if config.period is not None:
        return lc.fold(period=config.period)

    period_min = config.period_min or 0.5
    period_max = config.period_max or 30.0

    try:
        periodogram = lc.to_periodogram(  # type: ignore[attr-defined]
            method="bls",
            period_min=period_min,
            period_max=period_max,
        )
        period = getattr(periodogram.period_at_max_power, "value", None)
    except Exception as exc:  # pragma: no cover
        raise PreprocessingError("Failed to compute periodogram") from exc

    if period is None:
        raise PreprocessingError("Unable to determine period for phase fold")

    return lc.fold(period=period)


def _extract_array(values: Any) -> np.ndarray:
    if hasattr(values, "value"):
        return np.asarray(values.value)
    return np.asarray(values)


def preprocess_lightcurve(
    path: str | Path,
    *,
    flux_column: str = "PDCSAP_FLUX",
    config: PreprocessingConfig | None = None,
    artifact_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Load and preprocess a light curve file, returning tensors and metadata."""

    cfg = config or PreprocessingConfig()
    path = Path(path)
    LOGGER.info("Preprocessing light curve", extra={"path": str(path), **asdict(cfg)})

    lc = _load_lightcurve(path, flux_column)
    cleaned = _apply_cleaning(lc, cfg)
    folded = _phase_fold(cleaned, cfg)

    flux = _extract_array(folded.flux)
    time = _extract_array(folded.time)

    if np.isnan(flux).any():
        raise PreprocessingError("Preprocessed flux contains NaNs")

    result: dict[str, Any] = {
        "time": time.astype(np.float32),
        "flux": flux.astype(np.float32),
        "metadata": {
            "path": str(path.resolve()),
            "flux_column": flux_column,
            "config": asdict(cfg),
        },
    }

    if artifact_dir is not None:
        stats, plot_path = validate_preprocessed_output(
            time=time,
            flux=flux,
            artifact_dir=artifact_dir,
            filename=path.stem,
        )
        result["statistics"] = stats.to_dict()
        result["plot_path"] = str(plot_path)

    return result


__all__ = ["PreprocessingError", "preprocess_lightcurve", "PreprocessingConfig"]
