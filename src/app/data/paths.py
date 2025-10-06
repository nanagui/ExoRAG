"""Helpers for managing filesystem layout of datasets."""

from __future__ import annotations

import os
from pathlib import Path


_DEFAULT_DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def _base_dir() -> Path:
    """Resolve root directory for data assets."""

    custom_dir = os.getenv("EXOAI_DATA_DIR")
    if custom_dir:
        return Path(custom_dir).expanduser().resolve()
    return _DEFAULT_DATA_DIR


def get_data_dir(create: bool = True) -> Path:
    """Return base data directory, optionally creating it."""

    data_dir = _base_dir()
    if create:
        data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_raw_data_dir(mission: str | None = None, create: bool = True) -> Path:
    """Return path for raw mission data."""

    base = get_data_dir(create=create)
    if mission:
        base = base / "raw" / mission.lower()
    else:
        base = base / "raw"
    if create:
        base.mkdir(parents=True, exist_ok=True)
    return base


def get_processed_data_dir(mission: str | None = None, create: bool = True) -> Path:
    """Return path for processed datasets and tensors."""

    base = get_data_dir(create=create)
    if mission:
        base = base / "processed" / mission.lower()
    else:
        base = base / "processed"
    if create:
        base.mkdir(parents=True, exist_ok=True)
    return base


__all__ = [
    "get_data_dir",
    "get_raw_data_dir",
    "get_processed_data_dir",
]
