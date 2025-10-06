"""Utility script to log training runs to MLflow."""

from __future__ import annotations

import argparse
from pathlib import Path

import mlflow

from app.models.module import ModelConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log training artifacts to MLflow")
    parser.add_argument("run_name", help="Name of the MLflow run")
    parser.add_argument("--config", type=Path, default=Path("app/config/training.yaml"))
    parser.add_argument("--metrics", type=Path, help="Path to JSON metrics file", required=True)
    parser.add_argument("--artifacts", type=Path, nargs="*", help="Additional artifacts to log")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mlflow.set_experiment("exoai")
    with mlflow.start_run(run_name=args.run_name):
        mlflow.log_artifact(str(args.config))
        mlflow.log_artifact(str(args.metrics))
        if args.artifacts:
            for artifact in args.artifacts:
                mlflow.log_artifact(str(artifact))
        cfg = ModelConfig()
        mlflow.log_params(
            {
                "cnn_channels": cfg.cnn.conv_channels,
                "lstm_hidden": cfg.lstm.hidden_size,
                "physics_weight": cfg.physics_loss.weight,
            }
        )


if __name__ == "__main__":
    main()
