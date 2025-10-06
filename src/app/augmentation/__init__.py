"""Synthetic signal generation and oversampling helpers."""

from .config import SyntheticTransitConfig
from .transit import generate_transit_curve, inject_transit_signal
from .oversampling import apply_smote

__all__ = [
    "SyntheticTransitConfig",
    "generate_transit_curve",
    "inject_transit_signal",
    "apply_smote",
]
