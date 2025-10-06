PYTHON ?= python3.11
VENV ?= .venv
APP_MODULE ?= app.main:app
UVICORN_OPTS ?= --host 0.0.0.0 --port 8000

.PHONY: help install install-dev lint format typecheck test run docker-build docker-run

help:
	@echo "Available targets:"
	@echo "  install       - Create virtual env and install requirements"
	@echo "  install-dev   - Install requirements + pre-commit"
	@echo "  lint          - Run pre-commit hooks"
	@echo "  format        - Auto-format using black and isort"
	@echo "  typecheck     - Run mypy"
	@echo "  test          - Run pytest (placeholder)"
	@echo "  run           - Start FastAPI with uvicorn"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run Docker image"

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip

install: $(VENV)/bin/activate
	$(VENV)/bin/pip install -r requirements.txt

install-dev: install
	$(VENV)/bin/pip install pre-commit
	$(VENV)/bin/pre-commit install

lint:
	$(VENV)/bin/pre-commit run --all-files

format:
	$(VENV)/bin/black src
	$(VENV)/bin/isort src

typecheck:
	$(VENV)/bin/mypy src

test: $(VENV)/bin/activate
	PYTHONPATH=src $(VENV)/bin/pytest -q

run:
	$(VENV)/bin/uvicorn $(APP_MODULE) $(UVICORN_OPTS) --reload

docker-build:
	docker build -t exoai-app .

docker-run:
	docker run --rm --gpus all -p 8000:8000 exoai-app

train:
	PYTHONPATH=src $(VENV)/bin/python -m app.cli.train --config app/config/training.yaml

evaluate:
	PYTHONPATH=src $(VENV)/bin/python -m app.cli.evaluate --checkpoint data/artifacts/checkpoints/best.ckpt

baseline:
	PYTHONPATH=src $(VENV)/bin/python -c "from app.baselines.random_forest import train_random_forest; import pathlib; train_random_forest(pathlib.Path('data/manifests/train.jsonl'), pathlib.Path('data/manifests/val.jsonl'), save_path=pathlib.Path('data/artifacts/baselines/rf.joblib'))"

mlflow-track:
	PYTHONPATH=src $(VENV)/bin/python scripts/track_training.py $(RUN_NAME) --metrics $(METRICS) --artifacts $(ARTIFACTS)
