from __future__ import annotations

import importlib
from pathlib import Path

import pytest
from sqlmodel import select


@pytest.fixture
def temp_database(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("EXOAI_DATABASE_URL", f"sqlite:///{db_file}")

    from app.config import get_settings

    get_settings.cache_clear()

    import app.db.database as database_module
    import app.db.models as models_module

    importlib.reload(database_module)
    importlib.reload(models_module)

    from app.db.database import get_session, init_db

    init_db()
    yield

    get_settings.cache_clear()
    importlib.reload(database_module)


def test_record_lightcurve_downloads(temp_database):
    from app.db.database import get_session
    from app.db.models import LightCurveRecord
    from app.db.operations import record_lightcurve_downloads, record_preprocessing_result

    with get_session() as session:
        record_lightcurve_downloads(
            session,
            target="KIC 1234567",
            mission="Kepler",
            flux_type="PDCSAP_FLUX",
            records=[
                ("/tmp/kic1234567.fits", {"MISSION": "Kepler"}),
                ("/tmp/kic1234567-second.fits", None),
            ],
        )

    with get_session() as session:
        results = session.exec(select(LightCurveRecord).order_by(LightCurveRecord.path)).all()

    assert len(results) == 2
    assert results[0].target == "KIC 1234567"
    assert results[0].mission == "Kepler"
    assert results[0].source_metadata == {"MISSION": "Kepler"}

    # ensure update path refreshes timestamp rather than duplicating
    with get_session() as session:
        record_lightcurve_downloads(
            session,
            target="KIC 1234567",
            mission="Kepler",
            flux_type="SAP_FLUX",
            records=[("/tmp/kic1234567.fits", {"UPDATED": True})],
        )

    with get_session() as session:
        result = session.exec(
            select(LightCurveRecord).where(LightCurveRecord.path == "/tmp/kic1234567.fits")
        ).one()

        stats_record = record_preprocessing_result(
            session,
            path="/tmp/kic1234567.fits",
            stats={"mean": 0.0, "std": 1.0, "min": -1.0, "max": 1.0, "count": 100},
            figure_path="/tmp/plot.png",
        )

    assert result.source_metadata == {"UPDATED": True}
    assert result.flux_type == "SAP_FLUX"
    assert stats_record.figure_path == "/tmp/plot.png"
    assert stats_record.flux_count == 100
