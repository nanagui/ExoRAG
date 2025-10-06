from __future__ import annotations

import os
from pathlib import Path

import pytest

from app.data.paths import get_data_dir, get_processed_data_dir, get_raw_data_dir


@pytest.fixture(autouse=True)
def restore_env():
    original = os.environ.get("EXOAI_DATA_DIR")
    try:
        yield
    finally:
        if original is None:
            os.environ.pop("EXOAI_DATA_DIR", None)
        else:
            os.environ["EXOAI_DATA_DIR"] = original


def test_get_data_dir_defaults(tmp_path: Path) -> None:
    os.environ["EXOAI_DATA_DIR"] = str(tmp_path)
    data_dir = get_data_dir()
    assert data_dir == tmp_path
    assert data_dir.exists()


@pytest.mark.parametrize("mission", [None, "Kepler", "TESS"])
def test_get_raw_and_processed_dirs(tmp_path: Path, mission: str | None) -> None:
    os.environ["EXOAI_DATA_DIR"] = str(tmp_path)
    raw = get_raw_data_dir(mission=mission)
    processed = get_processed_data_dir(mission=mission)
    assert raw.exists() and processed.exists()
    if mission:
        assert mission.lower() in raw.as_posix()
        assert mission.lower() in processed.as_posix()
