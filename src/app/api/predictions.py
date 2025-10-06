"""Prediction-related endpoints."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel

from ..auth import User, require_roles
from ..config import get_settings
from ..db import get_session, record_preprocessing_result
from ..preprocessing import PreprocessingConfig, preprocess_lightcurve
from ..rag.pipeline import EvidenceGenerator
from ..services.inference import InferenceService
from .. import dependencies
from ..data.ingestion import IngestionRequest

router = APIRouter()


class PredictionRequest(BaseModel):
    path: str
    flux_column: str = "PDCSAP_FLUX"


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    attention: list[float]
    evidence: dict[str, Any] | None = None
    preprocessing: dict[str, Any]


class IngestionJobRequest(BaseModel):
    target: str
    mission: str | None = None
    author: str | None = None
    sector: int | None = None
    quarter: int | None = None
    campaign: int | None = None
    flux_type: str = "PDCSAP_FLUX"


@router.post("/predict", response_model=PredictionResponse)
async def predict_from_file(
    file: UploadFile = File(...),
    inference: InferenceService = Depends(dependencies.inference_dependency),
    evidence_generator: EvidenceGenerator = Depends(dependencies.evidence_dependency),
    user: User = Depends(require_roles("astronomer", "admin")),
) -> PredictionResponse:
    tmp_dir = Path("data/uploads")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / file.filename
    content = await file.read()
    tmp_path.write_bytes(content)

    preprocess_cfg = PreprocessingConfig()
    result = preprocess_lightcurve(tmp_path, config=preprocess_cfg, artifact_dir=Path("data/artifacts/preprocessing"))

    inputs = np.stack((result["time"], result["flux"]))
    prediction, probability, attention = inference.predict(inputs)

    stats = result.get("statistics")
    if stats:
        with get_session() as session:
            record_preprocessing_result(
                session,
                path=str(tmp_path),
                stats=stats,
                figure_path=result.get("plot_path"),
            )

    question = f"Does this light curve indicate an exoplanet transit? Prediction={prediction}"
    evidence = evidence_generator.generate(question)

    return PredictionResponse(
        prediction=prediction,
        probability=probability,
        attention=attention.tolist(),
        evidence=evidence,
        preprocessing={
            "statistics": stats,
            "plot_path": result.get("plot_path"),
        },
    )


@router.get("/candidates")
async def list_candidates(user: User = Depends(require_roles("analyst", "astronomer", "admin"))):
    from sqlalchemy import select

    from ..db import get_session
    from ..db.models import LightCurveRecord

    with get_session() as session:
        records = (
            session.exec(
                select(LightCurveRecord).order_by(LightCurveRecord.downloaded_at.desc()).limit(20)
            ).all()
        )
    return [
        {
            "target": record.target,
            "mission": record.mission,
            "path": record.path,
            "downloaded_at": record.downloaded_at.isoformat(),
        }
        for record in records
    ]


@router.post("/stream")
async def stream_placeholder():  # pragma: no cover - placeholder for future streaming support
    return {"status": "not_implemented", "detail": "Real-time streaming will be available soon."}


@router.post("/ingest")
async def enqueue_ingestion_job(
    payload: IngestionJobRequest,
    user: User = Depends(require_roles("admin", "astronomer")),
):
    queue = dependencies.get_ingestion_queue()
    service = dependencies.get_ingestion_service()
    request = IngestionRequest(
        target=payload.target,
        mission=payload.mission,
        author=payload.author,
        sector=payload.sector,
        quarter=payload.quarter,
        campaign=payload.campaign,
        flux_type=payload.flux_type,
    )
    await queue.enqueue(service.fetch, request)
    return {"status": "queued", "target": payload.target}
