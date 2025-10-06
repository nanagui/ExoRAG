from __future__ import annotations

import numpy as np
import pytest

import app.augmentation.transit as transit_module
from app.augmentation.config import SyntheticTransitConfig
from app.augmentation.oversampling import apply_smote
from app.augmentation.transit import inject_transit_signal


class DummyTransitModel:
    def __init__(self, params, time, **kwargs):
        self.time = np.asarray(time)

    def light_curve(self, params):
        return np.ones_like(self.time) - 0.01


class DummyTransitParams:
    def __init__(self):
        self.t0 = None
        self.per = None
        self.rp = None
        self.a = None
        self.inc = None
        self.ecc = None
        self.w = None
        self.limb_dark = None
        self.u = None


class DummyBatman:
    TransitParams = DummyTransitParams
    TransitModel = DummyTransitModel


@pytest.fixture(autouse=True)
def patch_batman(monkeypatch):
    monkeypatch.setattr(transit_module, "batman", DummyBatman())
    yield


def test_generate_transit_curve_returns_expected_shape():
    time = np.linspace(0, 10, 50)
    cfg = SyntheticTransitConfig(period=5.0)
    curve = transit_module.generate_transit_curve(time, cfg)
    assert curve.shape == time.shape
    assert np.all(curve <= 1.0)


def test_inject_transit_signal_multiplicative(monkeypatch):
    time = np.linspace(0, 10, 10)
    flux = np.ones_like(time)
    cfg = SyntheticTransitConfig(depth_scale=0.5)
    result = inject_transit_signal(time, flux, config=cfg)
    assert result["flux"].shape == time.shape
    assert np.all(result["flux"] <= 1.0)


def test_apply_smote_balances_classes():
    features = np.array([[0.0], [1.0], [2.0]])
    labels = np.array([0, 0, 1])
    resampled_features, resampled_labels = apply_smote(features, labels, random_state=1, k_neighbors=1)
    _, counts = np.unique(resampled_labels, return_counts=True)
    assert set(counts) == {2}


def test_smote_requires_two_dimensional_features():
    with pytest.raises(ValueError):
        apply_smote(np.array([1.0, 2.0, 3.0]), np.array([0, 1, 1]))
