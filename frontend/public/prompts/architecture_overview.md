# Architecture Overview

```
                           +---------------------------+
                           |       React Dashboard     |
                           |  Vite / Plotly Frontend   |
                           +-------------+-------------+
                                         |
                                         | HTTP (JWT)
                                         v
+--------------------+       +-----------+-------------+       +-----------------------+
|  Background Jobs   |<----->|  FastAPI / Inference API |<---->|   Qdrant Vector Store  |
| - Async ingestion  |       |  (PyTorch + RAG)         |      +-----------------------+
| - Embedding refresh|       |    - Preprocessing       |              ^
+---------+----------+       |    - MLflow logging      |              |
          |                  +----+--------------+------+              |
          | Async Queue            |              |                     |
          v                        v              v                     |
+---------------------+    +----------------+  +----------------+       |
| NASA Light Curves   |    | SQLModel (Postgres) | MLflow Tracking |<----+
| (Kepler/TESS/K2)    |    |  Metadata + Stats   |   (optional)   |
+---------------------+    +----------------+  +----------------+
```

## Key Modules
- `app/src/app/data`: ingestion utilities + Earthaccess wrapper.
- `app/src/app/preprocessing`: cleaning, validation, synthetic augmentation.
- `app/src/app/models`: PyTorch data modules, hybrid architecture, Lightning module.
- `app/src/app/rag`: corpus ingestion, Qdrant index, LangChain evidence generator.
- `app/src/app/api`: FastAPI routers (predictions, metrics, ingest).
- `app/frontend`: React dashboard.

## Deployment (docker-compose)
- `api`: GPU-enabled backend container.
- `frontend`: static preview server for dashboard.
- `qdrant`: vector DB.
- `postgres`: metadata catalogue.

## Observability
- Structured JSON logging (structlog) with level from `EXOAI_LOG_LEVEL`.
- Prometheus `/metrics` endpoint for scraping.
- MLflow script for experiment tracking.
