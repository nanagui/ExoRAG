"""Database models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Column, ForeignKey, String, UniqueConstraint
from sqlmodel import Field, SQLModel


class LightCurveRecord(SQLModel, table=True):
    """Metadata about downloaded light curves."""

    __tablename__ = "light_curves"
    __table_args__ = (UniqueConstraint("path", name="uq_lightcurve_path"),)

    id: int | None = Field(default=None, primary_key=True)
    target: str = Field(index=True, min_length=1)
    mission: str | None = Field(default=None, index=True)
    path: str = Field(sa_column=Column(String(1024), nullable=False))
    flux_type: str = Field(default="PDCSAP_FLUX")
    download_status: str = Field(default="downloaded")
    downloaded_at: datetime = Field(default_factory=datetime.utcnow)
    source_metadata: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )


class PreprocessingRecord(SQLModel, table=True):
    """Statistics and artifacts generated during preprocessing."""

    __tablename__ = "preprocessing_records"

    id: int | None = Field(default=None, primary_key=True)
    lightcurve_id: int = Field(foreign_key="light_curves.id", index=True)
    flux_mean: float
    flux_std: float
    flux_min: float
    flux_max: float
    flux_count: int
    figure_path: str | None = Field(
        default=None,
        sa_column=Column(String(1024), nullable=True),
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)


__all__ = ["LightCurveRecord", "PreprocessingRecord"]
