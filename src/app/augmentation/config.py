"""Configuration objects for synthetic transit generation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SyntheticTransitConfig:
    period: float = 5.0  # days
    mid_transit_time: float = 0.0  # days
    semi_major_axis: float = 15.0  # stellar radii
    planet_radius: float = 0.1  # in stellar radii
    inclination: float = 88.0  # degrees
    eccentricity: float = 0.0
    omega: float = 90.0
    limb_darkening_model: str = "quadratic"
    limb_darkening_coeffs: tuple[float, float] = (0.1, 0.3)
    supersample_factor: int = 5
    exposure_time: float = 0.020417  # days (≈30 min)
    depth_scale: float = 1.0

