"""CLI to evaluate trained checkpoints on a manifest."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pytorch_lightning as pl
import torch
import yaml

from app.models.datasets import LightCurveDataModule
from app.models.module import ExoplanetClassifier, ModelConfig, OptimizerConfig
from app.models.architecture import CNNConfig, BiLSTMConfig
from app.models.losses import PhysicsLossConfig
from app.utils.manifests import load_manifest


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a checkpoint on a manifest")
    parser.add_argument("checkpoint", type=Path, help="Path to .ckpt file")
    parser.add_argument("--config", type=Path, default=Path("app/config/training.yaml"))
    parser.add_argument("--manifest", type=Path, default=None, help="Override test manifest")
    return parser.parse_args()


def _load_cfg(path: Path) -> dict[str, Any]:
    with path.open() as fh:
        return yaml.safe_load(fh)


def _model_from_cfg(cfg: dict[str, Any]) -> ModelConfig:
    return ModelConfig(
        cnn=CNNConfig(**cfg.get("cnn", {})),
        lstm=BiLSTMConfig(**cfg.get("lstm", {})),
        num_classes=cfg.get("num_classes", 2),
        physics_loss=PhysicsLossConfig(**cfg.get("physics_loss", {})),
        optimizer=OptimizerConfig(**cfg.get("optimizer", {})),
    )


def main() -> None:
    args = _parse_args()
    cfg = _load_cfg(args.config)

    manifest_path = args.manifest or cfg["paths"].get("test_manifest")
    if manifest_path is None:
        raise ValueError("Test manifest must be provided via --manifest or config paths.test_manifest")

    test_records = load_manifest(manifest_path)
    dm = LightCurveDataModule(
        train_records=[],
        val_records=[],
        test_records=test_records,
        batch_size=cfg.get("batch_size", 64),
        num_workers=cfg.get("num_workers", 8),
        sequence_length=cfg.get("sequence_length", 2000),
    )
    dm.setup()

    model = ExoplanetClassifier(config=_model_from_cfg(cfg))
    trainer = pl.Trainer(accelerator="gpu" if torch.cuda.is_available() else "cpu", devices=1)
    trainer.test(model=model, dataloaders=dm.test_dataloader(), ckpt_path=str(args.checkpoint))


if __name__ == "__main__":
    main()
