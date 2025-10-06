# Developer Onboarding Guide

## Prerequisites
- Python 3.11
- Node.js 20+
- Docker (for local stack) and docker-compose
- Access to NASA Earthdata credentials (optional for protected datasets)

## Setup Steps
1. **Clone & Environment**
   ```bash
   python -m venv app/.venv
   source app/.venv/bin/activate
   pip install -r app/requirements.txt
   pip install pre-commit
   pre-commit install
   ```
2. **Configure Environment Variables**
   - Copy `app/.env.example` to `app/.env` and populate NASA Earthdata credentials, Qdrant URL (or leave default to use docker-compose), JWT secret, etc.
3. **Database Migration**
   ```bash
   cd app
   PYTHONPATH=src python -c "from app.db.database import init_db; init_db()"
   ```
4. **Run API Locally**
   ```bash
   make install-dev
   make run
   ```
5. **Run Frontend**
   ```bash
   cd app/frontend
   npm install
   npm run dev -- --open
   ```
6. **Full Stack via Docker**
   ```bash
   cd app
   docker-compose up --build
   ```

## Testing & Quality Gates
- `make lint`, `make typecheck`, `make test`
- Frontend: `npm run lint`, `npm run build`

## Training Workflow
- Use `make train` with manifests prepared in `data/manifests`.
- Log metrics to MLflow using `make mlflow-track RUN_NAME=my-run METRICS=metrics.json ARTIFACTS="outputs/fig1.png"`.

## Common Pitfalls
- Ensure Qdrant is reachable before hitting `/predictions/predict` if evidence generation is required.
- JWT tokens must be present in `Authorization` header; generate via `create_access_token` utility until auth service is implemented.
- Attention heatmaps require backend to expose `attention` arrays; partial support exists but UI wiring pending.
