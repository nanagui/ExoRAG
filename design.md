# System Design Overview

## 1. Architectural Vision
The solution is composed of four macro-domains:
1. **Data Layer** – ingestion pipelines for NASA missions and scientific corpora.
2. **Modeling Layer** – hybrid deep learning model with physics-informed loss and supporting trainers.
3. **Knowledge Layer** – retrieval-augmented validation (embeddings, Qdrant, LLM agent).
4. **Application Layer** – FastAPI services, web dashboard, and observability components.

```
+-------------------------+                +-----------------------------+
|  NASA Data Sources      |                |  NASA Literature & Archives |
| - Kepler DR25 (MAST)    |                | - ADS papers, Exoplanet DB  |
| - TESS sectors          |                | - Mission docs              |
| - K2 light curves       |                |                             |
| - SDO / others (via     |                |                             |
|   earthaccess)          |                |                             |
+-----------+-------------+                +-------------+---------------+
            |                                           |
            v                                           v
   +-------------------+        Metadata        +-------------------+
   | Data Ingestion    |----------------------->| Knowledge Builder |
   | Pipelines         |<-------References------+   (Embeddings)    |
   +-------------------+                        +---------+---------+
            |                                            |
            v                                            v
   +-------------------+      Training Data      +-------------------+
   | Preprocessing &   |-----------------------> | Hybrid Model       |
   | Feature Engineering|                        | Trainer (PINN)    |
   +---------+---------+                        +---------+---------+
             |                                          |
             v                                          v
   +-------------------+   Inference + Evidence  +-------------------+
   | FastAPI Services  |<------------------------| RAG Validation     |
   | & Stream Workers  |------------------------>| (Qdrant + LLM)    |
   +---------+---------+                         +---------+---------+
             |                                               |
             v                                               v
   +-------------------+                         +-------------------+
   | Web Dashboard     |                         | Observability     |
   | (React/Plotly)    |                         | (Logs, Metrics)   |
   +-------------------+                         +-------------------+
```

## 2. Module Breakdown

### 2.1 Data Ingestion
- **NASA MAST Access:** Use Lightkurve/astroquery for Kepler, K2, TESS light curves.
- **earthaccess Integration:** Provide optional pipeline to authenticate with NASA Earthdata and download complementary datasets (e.g., SDO ML repository) for future multimodal experiments.
- **Metadata Store:** Persist dataset descriptors and provenance in PostgreSQL or SQLite + Parquet catalogs.

### 2.2 Preprocessing & Feature Engineering
- Implement wrappers around Lightkurve to detrend, remove outliers, normalize, and phase-fold curves.
- Generate synthetic transits using PyTransit/BATMAN; combine with SMOTE for class balance.
- Compute auxiliary features (transit depth, duration, period estimates) for physics module.

### 2.3 Hybrid Model Trainer
- Core network: CNN stack → BiLSTM → attention pooling → dense classifier.
- Physics-informed component: custom loss module accepting stellar parameters and predicted transit descriptors.
- Training orchestration: PyTorch Lightning (or custom loops) with mixed precision, checkpointing, metric logging (Weights & Biases or MLflow).

### 2.4 Retrieval-Augmented Validation
- Embedding model: BGE-M3 (sentence transformer) for both textual abstracts and numeric descriptors converted to textual prompts.
- Vector store: Qdrant configured with HNSW index, <10 ms query latency.
- LLM Orchestrator: LangChain-based agent that consumes retrieved context and produces natural-language validations and anomaly warnings.

### 2.5 Application & Serving
- **FastAPI:**
  - `/predict` for batch scoring.
  - `/stream` (WebSocket) for near real-time ingestion.
  - `/explain` for retrieving attention maps, physics residuals, and RAG citations.
- **Workers:** Background tasks for dataset ingestion, embedding refresh, and scheduled retraining.
- **Authentication:** OAuth2/JWT minimal implementation (future: NASA SSO integration).

### 2.6 Web Dashboard
- React + Plotly for visualizing raw vs processed light curves, attention highlights, and RAG summaries.
- Admin section for monitoring pipeline health and dataset ingestion status.

### 2.7 Observability & DevOps
- Containerization with Docker (GPU-enabled base images).
- Logging via Structured JSON (FastAPI, training pipeline).
- Metrics via Prometheus-compatible exporters.
- CI/CD hooks for linting, tests, and automated documentation builds.

## 3. Data Flow
1. Ingestion jobs download raw FITS/CSV files, optionally authenticating through earthaccess for protected datasets.
2. Preprocessing transforms raw curves into standardized tensors and features; synthetic signals augment positives.
3. Training loop consumes prepared datasets, optimizes hybrid model with physics loss, and logs metrics/checkpoints.
4. Post-training, inference service loads the best checkpoint, exposes REST/WebSocket endpoints, and streams predictions.
5. Each prediction triggers embedding generation → Qdrant query → LLM justification, which is returned with attention heatmaps to the client.
6. User feedback (annotations/labels) is captured for continual learning.

## 4. Technology Stack
- **Languages:** Python (backend, ML), TypeScript (frontend).
- **Key Libraries:** PyTorch, PyTorch Lightning, Lightkurve, Astropy, PyTransit/BATMAN, imbalanced-learn, sentence-transformers (BGE-M3), Qdrant client, LangChain, FastAPI, SQLModel/SQLAlchemy, Plotly, React.
- **Infrastructure:** Docker, docker-compose, optional Kubernetes manifests, NVIDIA CUDA, MLflow/W&B, Prometheus/Grafana.

## 5. Security & Compliance Considerations
- Earthaccess credentials stored via environment secrets; refresh tokens rotated automatically.
- Data usage adheres to NASA open data policies; audit logs track dataset versions and downstream usage.
- User accounts follow least-privilege model; sensitive operations (model retraining, dataset deletion) gated by admin roles.

## 6. Roadmap Highlights
- MVP: Offline ingestion + preprocessing + baseline model evaluation + FastAPI endpoint.
- Phase 2: Integrate physics loss, RAG, and Qdrant.
- Phase 3: Productionize dashboard, observability, and citizen science workflows.

