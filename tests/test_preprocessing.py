from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pytest

from app.preprocessing import (
    PreprocessingConfig,
    PreprocessingError,
    preprocess_lightcurve,
)


@dataclass
class DummyValue:
    value: np.ndarray


class DummyLightCurve:
    def __init__(self, flux: np.ndarray, time: np.ndarray) -> None:
        self.flux = DummyValue(flux)
        self.time = DummyValue(time)
        self._removed_outliers = False
        self._normalized = False
        self._flattened = False
        self._folded_period = None

    def remove_outliers(self, sigma: float):
        self._removed_outliers = True
        return self

    def remove_nans(self):
        return self

    def flatten(self, window_length: int):
        self._flattened = True
        return self

    def normalize(self):
        self._normalized = True
        return self

    def fold(self, period: float):
        self._folded_period = period
        return self

    def to_periodogram(self, method: str, period_min: float, period_max: float):
        class _Periodogram:
            def __init__(self, value: float) -> None:
                self.period_at_max_power = DummyValue(np.array([value]))

        return _Periodogram(value=2.5)


def test_preprocess_lightcurve_basic(monkeypatch, tmp_path):
    data_path = tmp_path / "curve.fits"
    data_path.write_text("dummy")

    dummy = DummyLightCurve(flux=np.ones(10), time=np.arange(10))

    monkeypatch.setattr("app.preprocessing.pipeline._load_lightcurve", lambda path, flux_column: dummy)
    monkeypatch.setattr("app.preprocessing.pipeline._ensure_lightkurve", lambda: None)

    cfg = PreprocessingConfig(phase_fold=False)
    artifact_dir = tmp_path / "artifacts"
    result = preprocess_lightcurve(data_path, config=cfg, artifact_dir=artifact_dir)

    assert result["flux"].dtype == np.float32
    assert result["time"].dtype == np.float32
    assert result["metadata"]["path"].endswith("curve.fits")
    assert dummy._removed_outliers is True
    assert dummy._normalized is True
    assert "statistics" in result
    assert "plot_path" in result
    assert Path(result["plot_path"]).exists()


def test_preprocess_lightcurve_with_phase_fold(monkeypatch, tmp_path):
    data_path = tmp_path / "curve.fits"
    data_path.write_text("dummy")
    dummy = DummyLightCurve(flux=np.ones(5), time=np.arange(5))

    monkeypatch.setattr("app.preprocessing.pipeline._load_lightcurve", lambda path, flux_column: dummy)
    monkeypatch.setattr("app.preprocessing.pipeline._ensure_lightkurve", lambda: None)

    cfg = PreprocessingConfig(phase_fold=True, period=None, period_min=1.0, period_max=5.0)
    preprocess_lightcurve(data_path, config=cfg)
    assert dummy._folded_period == 2.5


def test_preprocess_lightcurve_nan_failure(monkeypatch, tmp_path):
    data_path = tmp_path / "curve.fits"
    data_path.write_text("dummy")
    flux = np.array([1.0, np.nan, 3.0])
    dummy = DummyLightCurve(flux=flux, time=np.arange(3))

    monkeypatch.setattr("app.preprocessing.pipeline._load_lightcurve", lambda path, flux_column: dummy)
    monkeypatch.setattr("app.preprocessing.pipeline._ensure_lightkurve", lambda: None)

    cfg = PreprocessingConfig(phase_fold=False)
    with pytest.raises(PreprocessingError):
        preprocess_lightcurve(data_path, config=cfg)
