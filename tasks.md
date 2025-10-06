# Development Task Board

## Legend
- `[ ]` To do
- `[~]` In progress
- `[x]` Done

## Sprint 0 – Foundations
- [x] Set up Python project structure (`app/src`, virtualenv, pre-commit hooks).
- [x] Add core dependencies (`requirements.txt`) including lightkurve, pytorch, qdrant-client, langchain, `earthaccess`, etc.
- [x] Configure `.env` template and secrets handling for NASA/earthaccess credentials.
- [x] Provision Dockerfile with CUDA base image and FastAPI entry point.

## Data & Preprocessing
- [x] Implement data ingestion service for Kepler/TESS/K2 using Lightkurve/astroquery.
- [x] Prototype `earthaccess` authenticated download workflow for supplemental datasets (document usage + store tokens securely).
- [x] Build metadata catalog (e.g., SQLite + SQLModel) for tracking light curves and preprocessing status.
- [x] Implement preprocessing pipeline (detrend, outlier removal, normalization, phase folding) with logging and unit tests.
- [x] Create synthetic transit generator (PyTransit/BATMAN) and SMOTE augmentation pipeline.
- [x] Validate preprocessing outputs (statistics, plots) and write automated regression tests.

## Modeling
- [x] Define PyTorch data module for batched light curves and metadata features.
- [x] Implement CNN-BiLSTM-Attention architecture.
- [x] Implement physics-informed loss module enforcing Kepler constraints.
- [x] Configure training loop (PyTorch Lightning or custom) with mixed precision, checkpointing, and metric logging.
- [x] Set up hyperparameter configuration (YAML) and CLI entry point.
- [x] Build evaluation scripts for cross-mission validation (train/test splits, metrics export).
- [x] Prepare fallback Random Forest baseline for emergency demo.

## Retrieval-Augmented Validation
- [x] Curate corpus of NASA publications and confirmed exoplanet summaries (ADS, NASA Archive).
- [x] Generate embeddings with BGE-M3; populate Qdrant instance.
- [x] Implement RAG pipeline (LangChain) that consumes prediction context and returns citations/justifications.
- [x] Integrate RAG outputs into inference response schema; include confidence scoring.

## Serving & API
- [x] Implement FastAPI endpoints (`/predict`, `/stream`, `/explain`, `/candidates`).
- [x] Add background worker (Celery or asyncio tasks) for ingestion jobs and scheduled embedding refresh.
- [x] Implement authentication/authorization (JWT + role management).
- [x] Add health-check and metrics endpoints (Prometheus format).

## Web Dashboard
- [x] Scaffold React app with routing and authentication guard.
- [x] Implement light curve visualization (Plotly) with toggles raw vs processed. *(heatmap pending backend exposure)*
- [ ] Implement attention heatmap overlay and physics diagnostics view.
- [x] Display RAG citations with links and confidence badges.
- [ ] Build citizen scientist workflow (submit new curve, annotate, flag for astronomers).

## Observability & Ops
- [x] Configure structured logging (Python + frontend) and central log aggregation.
- [x] Set up model version tracking (MLflow or W&B) and artifact storage.
- [x] Write docker-compose for local stack (API, Qdrant, Postgres, frontend).
- [x] Prepare CI pipeline (GitHub Actions) covering linting, tests, container build.

## Documentation & Compliance
- [x] Document data licensing and attribution requirements for each NASA source.
- [x] Write onboarding guide for developers (setup, credentials, sample commands).
- [x] Draft user guide for astronomers and citizen scientists (submit, interpret outputs).
- [x] Maintain changelog and architecture diagrams as components evolve.
