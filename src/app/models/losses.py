"""Physics-informed loss components."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(slots=True)
class PhysicsLossConfig:
    weight: float = 0.1
    epsilon: float = 1e-6


class PhysicsInformedLoss(nn.Module):
    """Penalizes deviations from expected transit depth ratios."""

    def __init__(self, config: PhysicsLossConfig | None = None) -> None:
        super().__init__()
        self.config = config or PhysicsLossConfig()

    def forward(
        self,
        flux: torch.Tensor,
        expected_depth: torch.Tensor,
    ) -> torch.Tensor:
        """Compute weighted L1 penalty between observed and expected depths.

        Parameters
        ----------
        flux: Tensor of shape (batch, sequence_len)
            Normalized flux values for each sample.
        expected_depth: Tensor of shape (batch,)
            Target transit depths derived from astrophysical constraints.
        """

        if flux.ndim != 2:
            raise ValueError("Flux tensor must be 2D (batch, sequence_len)")

        baseline = flux.mean(dim=1)
        min_flux, _ = flux.min(dim=1)
        observed_depth = torch.clamp((baseline - min_flux) / (baseline + self.config.epsilon), 0.0, 1.0)
        loss = torch.mean(torch.abs(observed_depth - expected_depth))
        return self.config.weight * loss


__all__ = ["PhysicsInformedLoss", "PhysicsLossConfig"]
