"""Synthetic transit generation using the batman package."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

import numpy as np

from .config import SyntheticTransitConfig

try:  # pragma: no cover - optional heavy dependency
    import batman  # type: ignore
except ImportError:  # pragma: no cover
    batman = None  # type: ignore


class SyntheticTransitError(RuntimeError):
    """Raised when synthetic signal generation fails."""


def _ensure_batman() -> None:
    if batman is None:  # pragma: no cover
        raise ImportError(
            "batman-package is required for synthetic transit generation. Install dependencies first."
        )


def generate_transit_curve(
    time: Iterable[float] | np.ndarray,
    config: SyntheticTransitConfig | None = None,
) -> np.ndarray:
    """Generate a normalized transit light curve for the given time array."""

    _ensure_batman()
    cfg = config or SyntheticTransitConfig()
    params = batman.TransitParams()
    params.t0 = cfg.mid_transit_time
    params.per = cfg.period
    params.rp = cfg.planet_radius
    params.a = cfg.semi_major_axis
    params.inc = cfg.inclination
    params.ecc = cfg.eccentricity
    params.w = cfg.omega
    params.limb_dark = cfg.limb_darkening_model
    params.u = list(cfg.limb_darkening_coeffs)

    model = batman.TransitModel(
        params,
        time,
        supersample_factor=cfg.supersample_factor,
        exp_time=cfg.exposure_time,
    )
    curve = np.asarray(model.light_curve(params), dtype=np.float32)
    return curve


def inject_transit_signal(
    time: np.ndarray,
    flux: np.ndarray,
    *,
    config: SyntheticTransitConfig | None = None,
    noise_std: float | None = None,
) -> dict[str, np.ndarray]:
    """Inject a synthetic transit into the provided flux array."""

    cfg = config or SyntheticTransitConfig()
    if time.shape != flux.shape:
        raise SyntheticTransitError("Time and flux arrays must have identical shape")

    transit = generate_transit_curve(time, config=cfg)
    injected_flux = flux * (1.0 - cfg.depth_scale * (1.0 - transit))

    if noise_std is not None and noise_std > 0:
        injected_flux = injected_flux + np.random.normal(scale=noise_std, size=injected_flux.shape)

    return {
        "time": time.astype(np.float32),
        "flux": injected_flux.astype(np.float32),
        "transit_curve": transit.astype(np.float32),
        "metadata": asdict(cfg),
    }


__all__ = ["SyntheticTransitConfig", "generate_transit_curve", "inject_transit_signal", "SyntheticTransitError"]
