# Changelog

All notable changes to this project will be documented here.

## [0.1.0] - 2025-09-16
### Added
- Back-end FastAPI skeleton with structured logging and JWT-protected endpoints.
- Data ingestion via Lightkurve and Earthaccess wrapper; SQLModel metadata catalog.
- Preprocessing pipeline with validation artifacts and synthetic augmentation toolkit.
- PyTorch Lightning model (CNN-BiLSTM-Attention + physics loss) and Random Forest baseline.
- RAG stack (corpus ingestion, Qdrant index, LangChain evidence generator).
- React dashboard with candidate table, Plotly visualization, and evidence panel.
- Observability assets: docker-compose, GitHub Actions CI, MLflow tracking script, Prometheus metrics.

### Pending
- Attention heatmap overlay + citizen scientist workflow.
- Dedicated auth service to issue JWTs.
- Websocket streaming for near real-time ingestion feedback.
