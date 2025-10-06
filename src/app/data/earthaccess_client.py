"""Thin wrapper around the `earthaccess` library for authenticated downloads."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from ..config import get_settings

try:  # pragma: no cover - import guard for optional dependency
    import earthaccess  # type: ignore
except ImportError:  # pragma: no cover - runtime handled by wrapper
    earthaccess = None  # type: ignore


@dataclass(slots=True)
class EarthAccessCredentials:
    """Credential container for NASA Earthdata authentication."""

    token: str | None = None
    username: str | None = None
    password: str | None = None

    def has_token(self) -> bool:
        return bool(self.token)

    def has_credentials(self) -> bool:
        return bool(self.username and self.password)


class EarthAccessClient:
    """Convenience helper for logging in and downloading datasets via earthaccess."""

    def __init__(self, credentials: EarthAccessCredentials | None = None) -> None:
        settings = get_settings()
        if credentials is None:
            credentials = EarthAccessCredentials(
                token=settings.earthdata_token,
                username=settings.earthdata_username,
                password=settings.earthdata_password,
            )
        self._credentials = credentials
        self._logged_in = False

    @property
    def credentials(self) -> EarthAccessCredentials:
        if self._credentials is None or not (
            self._credentials.has_token() or self._credentials.has_credentials()
        ):
            raise RuntimeError("Earthaccess credentials/token are not configured.")
        return self._credentials

    def _ensure_library(self) -> None:
        if earthaccess is None:  # pragma: no cover
            raise ImportError(
                "earthaccess library is not installed. Add it to requirements and reinstall."
            )

    def login(self) -> None:
        """Authenticate with NASA Earthdata using provided credentials."""

        self._ensure_library()
        if self._logged_in:
            return
        creds = self.credentials
        if creds.has_token():
            earthaccess.login(strategy="environment", token=creds.token, persist=True)
        elif creds.has_credentials():
            earthaccess.login(
                strategy="environment",
                username=creds.username,
                password=creds.password,
                persist=True,
            )
        else:  # pragma: no cover - safeguarded by property
            raise RuntimeError("No Earthdata token or username/password available.")
        self._logged_in = True

    def search(self, **query: object) -> Sequence[object]:
        """Run an earthaccess.search_data query and return the results."""

        self.login()
        results = earthaccess.search_data(**query)
        return results

    def download(self, results: Iterable[object], destination: Path) -> list[Path]:
        """Download search results into the provided destination directory."""

        self.login()
        destination.mkdir(parents=True, exist_ok=True)
        paths = earthaccess.download(results, local_path=str(destination))
        return [Path(p).resolve() for p in paths]


__all__ = ["EarthAccessClient", "EarthAccessCredentials"]
