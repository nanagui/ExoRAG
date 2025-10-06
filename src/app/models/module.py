"""Lightning module encapsulating training logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import torch
from torch import nn
from torch.optim import AdamW

try:  # pragma: no cover - optional dependency
    import pytorch_lightning as pl
    from torchmetrics.classification import F1Score, Precision, Recall
except ImportError:  # pragma: no cover
    pl = object  # type: ignore
    F1Score = Precision = Recall = Any  # type: ignore

from .architecture import CNNBiLSTMAttention, BiLSTMConfig, CNNConfig
from .losses import PhysicsInformedLoss, PhysicsLossConfig


@dataclass(slots=True)
class OptimizerConfig:
    learning_rate: float = 1e-4
    weight_decay: float = 1e-5


@dataclass(slots=True)
class ModelConfig:
    cnn: CNNConfig = field(default_factory=CNNConfig)
    lstm: BiLSTMConfig = field(default_factory=BiLSTMConfig)
    num_classes: int = 2
    physics_loss: PhysicsLossConfig = field(default_factory=PhysicsLossConfig)
    optimizer: OptimizerConfig = field(default_factory=OptimizerConfig)


class ExoplanetClassifier(pl.LightningModule):  # type: ignore[misc]
    """Hybrid classifier with physics-informed regularization."""

    def __init__(self, config: ModelConfig | None = None) -> None:
        super().__init__()
        self.config = config or ModelConfig()
        self.model = CNNBiLSTMAttention(
            cnn_cfg=self.config.cnn,
            lstm_cfg=self.config.lstm,
            num_classes=self.config.num_classes,
        )
        self.criterion = nn.CrossEntropyLoss()
        self.physics_loss = PhysicsInformedLoss(self.config.physics_loss)
        self.save_hyperparameters(self.config.__dict__)

        self.train_f1 = F1Score(task="binary", num_classes=self.config.num_classes)
        self.val_f1 = F1Score(task="binary", num_classes=self.config.num_classes)
        self.val_precision = Precision(task="binary", num_classes=self.config.num_classes)
        self.val_recall = Recall(task="binary", num_classes=self.config.num_classes)

    def forward(self, inputs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        return self.model(inputs)

    def _extract_expected_depth(self, batch: dict[str, Any]) -> torch.Tensor:
        metadata = batch.get("metadata")
        if metadata is None:
            return torch.zeros(batch["inputs"].size(0), device=self.device)
        expected = []
        for item in metadata:
            if isinstance(item, dict) and "expected_depth" in item:
                expected.append(float(item["expected_depth"]))
            else:
                expected.append(0.0)
        return torch.tensor(expected, dtype=torch.float32, device=self.device)

    def training_step(self, batch: dict[str, Any], batch_idx: int) -> torch.Tensor:
        inputs = batch["inputs"].to(self.device)
        labels = batch["label"].to(self.device)
        logits, attention = self(inputs)
        loss = self.criterion(logits, labels)

        expected_depth = self._extract_expected_depth(batch)
        if torch.any(expected_depth > 0):
            flux = inputs[:, 1, :]
            loss = loss + self.physics_loss(flux, expected_depth)

        preds = torch.argmax(logits, dim=1)
        self.train_f1(preds, labels)
        self.log("train_loss", loss, prog_bar=True)
        self.log("train_f1", self.train_f1, prog_bar=True)
        return loss

    def validation_step(self, batch: dict[str, Any], batch_idx: int) -> None:
        inputs = batch["inputs"].to(self.device)
        labels = batch["label"].to(self.device)
        logits, _ = self(inputs)
        loss = self.criterion(logits, labels)
        preds = torch.argmax(logits, dim=1)
        self.val_f1(preds, labels)
        self.val_precision(preds, labels)
        self.val_recall(preds, labels)
        self.log("val_loss", loss, prog_bar=True, sync_dist=True)
        self.log("val_f1", self.val_f1, prog_bar=True, sync_dist=True)
        self.log("val_precision", self.val_precision, sync_dist=True)
        self.log("val_recall", self.val_recall, sync_dist=True)

    def configure_optimizers(self):
        optimizer = AdamW(
            self.parameters(),
            lr=self.config.optimizer.learning_rate,
            weight_decay=self.config.optimizer.weight_decay,
        )
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode="max",
            factor=0.5,
            patience=3,
            verbose=True,
        )
        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "monitor": "val_f1",
                "interval": "epoch",
                "frequency": 1,
            },
        }


__all__ = ["ExoplanetClassifier", "ModelConfig", "OptimizerConfig"]
