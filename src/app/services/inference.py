"""Inference service wrapping the trained model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch

from app.models.module import ExoplanetClassifier, ModelConfig


@dataclass(slots=True)
class InferenceConfig:
    checkpoint_path: str | None = None
    device: str | None = None


class InferenceService:
    """Handles model loading and synchronous inference."""

    def __init__(self, config: InferenceConfig | None = None) -> None:
        self.config = config or InferenceConfig()
        device = self.config.device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.device = torch.device(device)
        self.model = self._load_model().to(self.device)
        self.model.eval()

    def _load_model(self) -> ExoplanetClassifier:
        checkpoint = self.config.checkpoint_path
        if checkpoint and Path(checkpoint).exists():
            return ExoplanetClassifier.load_from_checkpoint(checkpoint)  # type: ignore[arg-type]
        return ExoplanetClassifier(config=ModelConfig())

    def predict(self, inputs: np.ndarray) -> tuple[int, float, np.ndarray]:
        """Run inference on a single light-curve sample.

        Parameters
        ----------
        inputs : np.ndarray
            Array shaped (channels, sequence_length)
        """

        if inputs.ndim != 2:
            raise ValueError("Expected inputs with shape (channels, sequence_length)")
        tensor = torch.from_numpy(inputs).unsqueeze(0).to(self.device)
        with torch.no_grad():
            logits, attention = self.model(tensor)
            probabilities = torch.softmax(logits, dim=1)
        probability, prediction = torch.max(probabilities, dim=1)
        return (
            int(prediction.item()),
            float(probability.item()),
            attention.squeeze(0).detach().cpu().numpy(),
        )


__all__ = ["InferenceService", "InferenceConfig"]
