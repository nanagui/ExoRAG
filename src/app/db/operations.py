"""Database operations for light curve metadata."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlmodel import Session, select

from .models import LightCurveRecord, PreprocessingRecord


def record_lightcurve_downloads(
    session: Session,
    *,
    target: str,
    mission: str | None,
    flux_type: str,
    records: Iterable[tuple[str, dict | None]],
) -> None:
    """Insert or update light-curve metadata records."""

    for path, metadata in records:
        existing = session.exec(
            select(LightCurveRecord).where(LightCurveRecord.path == path)
        ).first()

        if existing:
            existing.downloaded_at = datetime.utcnow()
            existing.source_metadata = metadata
            existing.target = target or existing.target
            existing.mission = mission or existing.mission
            existing.flux_type = flux_type
        else:
            session.add(
                LightCurveRecord(
                    target=target,
                    mission=mission,
                    path=path,
                    flux_type=flux_type,
                    source_metadata=metadata,
                )
            )

    session.commit()


def record_preprocessing_result(
    session: Session,
    *,
    path: str,
    stats: dict[str, float],
    figure_path: str | None = None,
) -> PreprocessingRecord:
    """Persist preprocessing statistics associated with a light curve."""

    lightcurve = session.exec(
        select(LightCurveRecord).where(LightCurveRecord.path == path)
    ).first()

    if lightcurve is None:
        lightcurve = LightCurveRecord(
            target="unknown",
            mission=None,
            path=path,
            flux_type=stats.get("flux_type", "PDCSAP_FLUX"),
        )
        session.add(lightcurve)
        session.flush()

    record = PreprocessingRecord(
        lightcurve_id=lightcurve.id,  # type: ignore[arg-type]
        flux_mean=float(stats["mean"]),
        flux_std=float(stats["std"]),
        flux_min=float(stats["min"]),
        flux_max=float(stats["max"]),
        flux_count=int(stats["count"]),
        figure_path=figure_path,
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


__all__ = ["record_lightcurve_downloads", "record_preprocessing_result"]
