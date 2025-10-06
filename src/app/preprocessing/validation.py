"""Validation utilities for preprocessed light curves."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg", force=True)

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class PreprocessingStatistics:
    mean: float
    std: float
    min: float
    max: float
    count: int

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["mean"] = float(self.mean)
        data["std"] = float(self.std)
        data["min"] = float(self.min)
        data["max"] = float(self.max)
        data["count"] = int(self.count)
        return data


def compute_statistics(flux: np.ndarray) -> PreprocessingStatistics:
    if flux.ndim != 1:
        raise ValueError("Flux array must be one-dimensional")
    return PreprocessingStatistics(
        mean=float(np.mean(flux)),
        std=float(np.std(flux)),
        min=float(np.min(flux)),
        max=float(np.max(flux)),
        count=int(flux.size),
    )


def save_plot(time: np.ndarray, flux: np.ndarray, output_path: str | Path) -> Path:
    if time.shape != flux.shape:
        raise ValueError("Time and flux arrays must share the same shape")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(time, flux, marker="o", linestyle="-", linewidth=1, markersize=2)
    ax.set_xlabel("Time")
    ax.set_ylabel("Normalized Flux")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    LOGGER.info("Saved preprocessing plot", extra={"path": str(output_path)})
    return output_path


def validate_preprocessed_output(
    *,
    time: np.ndarray,
    flux: np.ndarray,
    artifact_dir: str | Path,
    filename: str,
) -> tuple[PreprocessingStatistics, Path]:
    stats = compute_statistics(flux)
    artifact_dir = Path(artifact_dir)
    plot_path = artifact_dir / f"{filename}.png"
    save_plot(time, flux, plot_path)
    return stats, plot_path


__all__ = [
    "PreprocessingStatistics",
    "compute_statistics",
    "save_plot",
    "validate_preprocessed_output",
]
