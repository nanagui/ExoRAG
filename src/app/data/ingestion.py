"""Light curve ingestion routines for NASA missions."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from ..config import get_settings
from ..db import get_session, record_lightcurve_downloads
from .paths import get_raw_data_dir

try:  # pragma: no cover - optional heavy dependency
    import lightkurve as lk
except ImportError:  # pragma: no cover
    lk = None  # type: ignore

LOGGER = logging.getLogger(__name__)

FluxType = Literal["PDCSAP_FLUX", "SAP_FLUX"]


@dataclass(slots=True)
class IngestionRequest:
    """Parameters describing a light curve retrieval job."""

    target: str
    mission: str | None = None
    author: str | None = None
    cadence: str | None = None
    quarter: int | None = None
    campaign: int | None = None
    sector: int | None = None
    flux_type: FluxType = "PDCSAP_FLUX"


class LightCurveIngestionService:
    """Download light curves using Lightkurve search interfaces."""

    def __init__(self, *, download_dir: Path | None = None) -> None:
        self.settings = get_settings()
        self.download_dir = download_dir

    def _ensure_lightkurve(self) -> None:
        if lk is None:  # pragma: no cover
            raise ImportError(
                "lightkurve library is required for ingestion. Install dependencies first."
            )

    def _resolve_directory(self, mission: str | None) -> Path:
        if self.download_dir is not None:
            path = self.download_dir
        else:
            path = get_raw_data_dir(mission=mission)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def fetch(self, request: IngestionRequest, *, limit: int | None = None) -> list[Path]:
        """Search and download light curves according to the request."""

        self._ensure_lightkurve()
        search_kwargs: dict[str, Any] = {
            "target": request.target,
            "mission": request.mission,
            "author": request.author,
            "cadence": request.cadence,
        }
        if request.quarter is not None:
            search_kwargs["quarter"] = request.quarter
        if request.campaign is not None:
            search_kwargs["campaign"] = request.campaign
        if request.sector is not None:
            search_kwargs["sector"] = request.sector

        LOGGER.info("Searching light curves", extra={"params": search_kwargs})
        search_result = lk.search_lightcurve(**search_kwargs)
        if limit is not None:
            search_result = search_result[:limit]

        destination = self._resolve_directory(request.mission or "unknown")
        LOGGER.info(
            "Downloading light curves",
            extra={
                "count": len(search_result),
                "destination": str(destination),
                "target": request.target,
            },
        )
        downloaded = search_result.download_all(
            download_dir=str(destination),
            flux_column=request.flux_type,
        )

        records: list[tuple[str, dict | None]] = []
        for lightcurve in downloaded:
            path: Path | None = None
            lc_path = getattr(lightcurve, "path", None)
            if lc_path:
                path = Path(lc_path)
            else:
                filename = (
                    lightcurve.meta.get("FILENAME")
                    or lightcurve.meta.get("ORIGIN_FILENAME")
                )
                if filename:
                    path = destination / filename
            if path is not None:
                path_str = str(path.resolve())
                metadata = getattr(lightcurve, "meta", None)
                if metadata is not None:
                    metadata = dict(metadata)
                records.append((path_str, metadata))

        if records:
            with get_session() as session:
                record_lightcurve_downloads(
                    session,
                    target=request.target,
                    mission=request.mission,
                    flux_type=request.flux_type,
                    records=records,
                )

        return [Path(path) for path, _ in records]


__all__ = ["IngestionRequest", "LightCurveIngestionService"]
