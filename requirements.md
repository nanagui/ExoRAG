# Functional and Non-Functional Requirements

## 1. Functional Requirements

### FR-1 Data Acquisition
- FR-1.1: The system shall download light curve datasets from NASA sources (Kepler DR25, K2, TESS sectors) using official APIs or bulk files.
- FR-1.2: The system shall support authenticated retrieval of supplementary NASA datasets through the `earthaccess` Python library when available (e.g., for SDO/other Earthdata resources).
- FR-1.3: The ingestion pipeline shall catalog metadata (sector, cadence, target ID, mission) for indexing and reproducibility.

### FR-2 Preprocessing & Feature Engineering
- FR-2.1: The system shall clean, detrend, normalize, and phase-fold light curves using Lightkurve-based routines or equivalent implementations.
- FR-2.2: The pipeline shall automatically remove NaNs/outliers and log preprocessing diagnostics.
- FR-2.3: The system shall generate synthetic transits via PyTransit/BATMAN and apply SMOTE to balance classes.

### FR-3 Model Training & Evaluation
- FR-3.1: The platform shall train a CNN-BiLSTM-Attention model with a physics-informed loss term enforcing Keplerian constraints.
- FR-3.2: The training process shall support cross-mission ensembling and configurable hyperparameters.
- FR-3.3: The system shall track metrics (F1, precision, recall, ROC-AUC) and store checkpoints.

### FR-4 Retrieval-Augmented Validation
- FR-4.1: The system shall embed predictions and metadata using BGE-M3 (or equivalent) and index them in Qdrant.
- FR-4.2: The platform shall query relevant NASA literature and confirmed exoplanets to generate textual justifications via an LLM.

### FR-5 Serving & User Experience
- FR-5.1: Provide a FastAPI service exposing inference endpoints, including batch scoring and real-time streaming.
- FR-5.2: Provide a web dashboard that visualizes raw/processed light curves, attention heatmaps, and citations returned by RAG.
- FR-5.3: Support user authentication/roles for astronomers vs citizen scientists (read-only vs annotation privileges).

### FR-6 Observability & Collaboration
- FR-6.1: Log processing steps, model decisions, and RAG evidence for auditability.
- FR-6.2: Allow export of candidate reports (PDF/JSON) summarizing AI decisions and physics checks.

## 2. Non-Functional Requirements

### NFR-1 Performance
- NFR-1.1: Inference latency shall be <100 ms per light curve on an NVIDIA RTX-class GPU.
- NFR-1.2: Data ingestion shall parallelize downloads to handle sector-scale datasets within acceptable time frames (<2 h per TESS sector subset).

### NFR-2 Reliability & Robustness
- NFR-2.1: Pipelines shall include validation checkpoints; failures must surface actionable error messages.
- NFR-2.2: Synthetic generation and SMOTE steps shall be reproducible (seeded).

### NFR-3 Scalability
- NFR-3.1: Architecture shall be containerized (Docker) and deployable to cloud GPUs.
- NFR-3.2: Qdrant and model services shall scale horizontally for increased workload.

### NFR-4 Security & Compliance
- NFR-4.1: Earthaccess authentication credentials must be stored securely (environment variables, secrets manager).
- NFR-4.2: Sensitive NASA data usage must comply with dataset licensing and attribution requirements.

### NFR-5 Maintainability
- NFR-5.1: Codebase shall include automated tests (unit + integration) for preprocessing, model interfaces, and API endpoints.
- NFR-5.2: CI pipeline shall run linting, tests, and model artifact validation before deployment.

### NFR-6 Explainability & Ethics
- NFR-6.1: System shall surface attention visualizations and physics-residual diagnostics for each prediction.
- NFR-6.2: RAG justifications shall reference original documents with citations and confidence scores.

