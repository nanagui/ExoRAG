from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from app.preprocessing.validation import (
    PreprocessingStatistics,
    compute_statistics,
    save_plot,
    validate_preprocessed_output,
)


def test_compute_statistics_returns_expected_values():
    flux = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    stats = compute_statistics(flux)
    assert isinstance(stats, PreprocessingStatistics)
    assert stats.mean == pytest.approx(2.0)
    assert stats.std == pytest.approx(np.std(flux))
    assert stats.min == pytest.approx(1.0)
    assert stats.count == 3


def test_save_plot_creates_file(tmp_path: Path):
    time = np.linspace(0, 1, 10)
    flux = np.linspace(1, 0, 10)
    path = save_plot(time, flux, tmp_path / "plot.png")
    assert path.exists()


def test_validate_preprocessed_output(tmp_path: Path):
    time = np.linspace(0, 1, 5)
    flux = np.ones(5)
    stats, plot_path = validate_preprocessed_output(
        time=time,
        flux=flux,
        artifact_dir=tmp_path,
        filename="curve",
    )
    assert stats.count == 5
    assert plot_path.exists()


def test_save_plot_requires_matching_shapes(tmp_path: Path):
    time = np.array([0, 1, 2])
    flux = np.array([1, 2])
    with pytest.raises(ValueError):
        save_plot(time, flux, tmp_path / "plot.png")
