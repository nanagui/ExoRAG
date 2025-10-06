"""CLI entry point for training the exoplanet classifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pytorch_lightning as pl
import torch
import yaml

from app.models.datasets import LightCurveDataModule
from app.models.module import ModelConfig, ExoplanetClassifier
from app.models.architecture import CNNConfig, BiLSTMConfig
from app.models.losses import PhysicsLossConfig
from app.models.module import OptimizerConfig
from app.utils.manifests import load_manifest


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the Exoplanet AI classifier")
    parser.add_argument("--config", type=Path, default=Path("app/config/training.yaml"), help="Path to training YAML")
    parser.add_argument("--overwrite-checkpoint", action="store_true", help="Overwrite existing checkpoints")
    return parser.parse_args()


def _load_yaml_config(path: Path) -> dict[str, Any]:
    with path.open() as fh:
        return yaml.safe_load(fh)


def _build_model_config(cfg: dict[str, Any]) -> ModelConfig:
    model_cfg = ModelConfig(
        cnn=CNNConfig(**cfg.get("cnn", {})),
        lstm=BiLSTMConfig(**cfg.get("lstm", {})),
        num_classes=cfg.get("num_classes", 2),
        physics_loss=PhysicsLossConfig(**cfg.get("physics_loss", {})),
        optimizer=OptimizerConfig(**cfg.get("optimizer", {})),
    )
    return model_cfg


def _prepare_datamodule(cfg: dict[str, Any], batch_size: int, sequence_length: int, num_workers: int) -> LightCurveDataModule:
    paths = cfg["paths"]
    train_records = load_manifest(paths["train_manifest"])
    val_records = load_manifest(paths["val_manifest"])
    test_manifest = paths.get("test_manifest")
    test_records = load_manifest(test_manifest) if test_manifest else []

    return LightCurveDataModule(
        train_records,
        val_records,
        test_records,
        batch_size=batch_size,
        num_workers=num_workers,
        sequence_length=sequence_length,
    )


def main() -> None:
    args = _parse_args()
    cfg = _load_yaml_config(args.config)

    seed = cfg.get("seed", 42)
    pl.seed_everything(seed, workers=True)

    dm = _prepare_datamodule(
        cfg,
        batch_size=cfg.get("batch_size", 64),
        sequence_length=cfg.get("sequence_length", 2000),
        num_workers=cfg.get("num_workers", 8),
    )

    model = ExoplanetClassifier(config=_build_model_config(cfg))

    trainer_cfg = cfg.get("trainer", {})
    checkpoint_dir = Path(trainer_cfg.get("checkpoints_dir", "data/artifacts/checkpoints"))
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    callbacks = []
    checkpoint_path = checkpoint_dir / "best.ckpt"
    if args.overwrite_checkpoint and checkpoint_path.exists():
        checkpoint_path.unlink()

    checkpoint_cb = pl.callbacks.ModelCheckpoint(
        dirpath=str(checkpoint_dir),
        filename="best",
        monitor="val_f1",
        mode="max",
        save_top_k=1,
        save_last=True,
    )
    callbacks.append(checkpoint_cb)
    early_stop_cb = pl.callbacks.EarlyStopping(monitor="val_f1", patience=5, mode="max")
    callbacks.append(early_stop_cb)

    trainer = pl.Trainer(
        max_epochs=cfg.get("max_epochs", 20),
        gradient_clip_val=trainer_cfg.get("gradient_clip_val", 1.0),
        log_every_n_steps=trainer_cfg.get("log_every_n_steps", 10),
        callbacks=callbacks,
        accelerator="gpu" if torch.cuda.is_available() else "cpu",
        devices=trainer_cfg.get("gpus", 1) if torch.cuda.is_available() else 1,
        accumulate_grad_batches=cfg.get("accumulate_grad_batches", 1),
        precision=cfg.get("precision", 16),
    )

    trainer.fit(model, datamodule=dm)

    if dm.test_records:
        trainer.test(model, datamodule=dm, ckpt_path="best")


if __name__ == "__main__":
    main()
