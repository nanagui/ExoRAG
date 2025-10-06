from __future__ import annotations

import io
from pathlib import Path
from typing import Any
from types import SimpleNamespace

import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.auth import create_access_token


class DummyInferenceService:
    def predict(self, inputs: np.ndarray):
        return 1, 0.95, np.ones(inputs.shape[1])


class DummyEvidenceGenerator:
    def generate(self, question: str) -> dict[str, Any]:
        return {"question": question, "answer": "Likely planet", "documents": []}


class DummyQueue:
    def __init__(self):
        self.enqueued = []

    async def enqueue(self, func, *args, **kwargs):
        self.enqueued.append((func, args, kwargs))


@pytest.fixture
def client(monkeypatch):
    dummy_queue = DummyQueue()

    from app import dependencies
    from app import workers

    monkeypatch.setattr(dependencies, "ensure_corpus_indexed", lambda: None)

    async def _noop():
        return None

    monkeypatch.setattr(workers.SCHEDULER, "start", _noop)
    monkeypatch.setattr(workers.SCHEDULER, "stop", _noop)

    app = create_app()

    monkeypatch.setattr(dependencies, "get_inference_service", lambda: DummyInferenceService())
    monkeypatch.setattr(dependencies, "get_evidence_generator", lambda retriever=None: DummyEvidenceGenerator())
    monkeypatch.setattr(dependencies, "inference_dependency", lambda: DummyInferenceService())
    monkeypatch.setattr(dependencies, "evidence_dependency", lambda: DummyEvidenceGenerator())
    monkeypatch.setattr(dependencies, "get_ingestion_queue", lambda: dummy_queue)
    monkeypatch.setattr(dependencies, "get_ingestion_service", lambda: SimpleNamespace(fetch=lambda request: None))

    from app.api import predictions

    monkeypatch.setattr(predictions, "preprocess_lightcurve", lambda *args, **kwargs: {
        "time": np.linspace(0, 1, 10, dtype=np.float32),
        "flux": np.linspace(1, 0, 10, dtype=np.float32),
        "statistics": {"mean": 0.5, "std": 0.1, "min": 0.0, "max": 1.0, "count": 10},
        "plot_path": "plot.png",
    })
    monkeypatch.setattr(predictions, "record_preprocessing_result", lambda *args, **kwargs: None)

    test_client = TestClient(app)
    test_client.app.state.dummy_queue = dummy_queue  # type: ignore[attr-defined]
    return test_client


def test_health_endpoint(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics_endpoint(client: TestClient):
    response = client.get("/api/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")


def test_predict_endpoint(client: TestClient, tmp_path: Path):
    file_content = b"dummy"
    token = create_access_token(subject="tester", roles=["astronomer"])
    response = client.post(
        "/api/predictions/predict",
        files={"file": ("sample.fits", file_content, "application/octet-stream")},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["prediction"] == 1
    assert payload["probability"] == pytest.approx(0.95, rel=1e-3)
    assert len(payload["attention"]) == 10
    assert payload["evidence"]["answer"].startswith("Likely")


def test_candidates_endpoint(client: TestClient):
    token = create_access_token(subject="tester", roles=["analyst"])
    response = client.get("/api/predictions/candidates", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ingestion_enqueue(client: TestClient):
    token = create_access_token(subject="tester", roles=["astronomer"])
    payload = {"target": "KIC 1234567", "mission": "Kepler"}
    response = client.post(
        "/api/predictions/ingest",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    queue = client.app.state.dummy_queue  # type: ignore[attr-defined]
    assert len(queue.enqueued) == 1
