from __future__ import annotations

from pathlib import Path

import pytest

import app.data.earthaccess_client as ec_module
from app.data.earthaccess_client import EarthAccessClient


class DummyEarthaccess:
    def __init__(self) -> None:
        self.logged_in = False
        self.download_calls = []
        self.credentials = None

    def login(self, **kwargs):
        self.logged_in = True
        self.credentials = kwargs

    def search_data(self, **query):
        self.last_query = query
        return ["file1", "file2"]

    def download(self, results, local_path: str):
        Path(local_path).mkdir(parents=True, exist_ok=True)
        self.download_calls.append((tuple(results), local_path))
        return [str(Path(local_path) / name) for name in results]


def test_client_uses_credentials(monkeypatch, tmp_path):
    dummy = DummyEarthaccess()
    monkeypatch.setenv("EXOAI_EARTHDATA_USERNAME", "user")
    monkeypatch.setenv("EXOAI_EARTHDATA_PASSWORD", "secret")

    monkeypatch.setattr(ec_module, "earthaccess", dummy, raising=False)
    monkeypatch.setattr(EarthAccessClient, "_ensure_library", lambda self: None, raising=False)

    from app.config import get_settings

    get_settings.cache_clear()

    client = EarthAccessClient()
    results = client.search(short_name="SDO")
    assert dummy.logged_in is True
    assert dummy.credentials["username"] == "user"
    assert results == ["file1", "file2"]

    files = client.download(results, destination=tmp_path)
    assert len(files) == 2
    assert Path(files[0]).exists()

    get_settings.cache_clear()


def test_missing_credentials_error(monkeypatch):
    monkeypatch.delenv("EXOAI_EARTHDATA_USERNAME", raising=False)
    monkeypatch.delenv("EXOAI_EARTHDATA_PASSWORD", raising=False)

    from app.config import get_settings

    get_settings.cache_clear()
    client = EarthAccessClient(credentials=None)

    with pytest.raises(RuntimeError):
        _ = client.credentials

    get_settings.cache_clear()
