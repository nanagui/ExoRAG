"""Model architectures for light-curve classification."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(slots=True)
class CNNConfig:
    in_channels: int = 2
    conv_channels: tuple[int, ...] = (32, 64, 128)
    kernel_sizes: tuple[int, ...] = (7, 5, 3)
    pool_size: int = 2
    dropout: float = 0.1


@dataclass(slots=True)
class BiLSTMConfig:
    hidden_size: int = 128
    num_layers: int = 1
    dropout: float = 0.1


class AttentionPool(nn.Module):
    """Simple additive attention over temporal dimension."""

    def __init__(self, hidden_dim: int) -> None:
        super().__init__()
        self.query = nn.Linear(hidden_dim, hidden_dim)
        self.context_vector = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, inputs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        # inputs: (batch, seq, hidden)
        scores = torch.tanh(self.query(inputs))
        attention = torch.softmax(self.context_vector(scores), dim=1)
        context = torch.sum(attention * inputs, dim=1)
        return context, attention.squeeze(-1)


class CNNBiLSTMAttention(nn.Module):
    """Hybrid CNN + BiLSTM + Attention backbone."""

    def __init__(
        self,
        cnn_cfg: CNNConfig | None = None,
        lstm_cfg: BiLSTMConfig | None = None,
        *,
        num_classes: int = 2,
    ) -> None:
        super().__init__()
        cnn_cfg = cnn_cfg or CNNConfig()
        lstm_cfg = lstm_cfg or BiLSTMConfig()

        layers = []
        in_channels = cnn_cfg.in_channels
        seq_reduction = 1
        for out_channels, kernel in zip(cnn_cfg.conv_channels, cnn_cfg.kernel_sizes):
            layers.append(nn.Conv1d(in_channels, out_channels, kernel_size=kernel, padding=kernel // 2))
            layers.append(nn.BatchNorm1d(out_channels))
            layers.append(nn.ReLU())
            layers.append(nn.MaxPool1d(kernel_size=cnn_cfg.pool_size))
            layers.append(nn.Dropout(cnn_cfg.dropout))
            in_channels = out_channels
            seq_reduction *= cnn_cfg.pool_size

        self.cnn = nn.Sequential(*layers)
        self.lstm = nn.LSTM(
            input_size=in_channels,
            hidden_size=lstm_cfg.hidden_size,
            num_layers=lstm_cfg.num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=lstm_cfg.dropout if lstm_cfg.num_layers > 1 else 0.0,
        )
        self.attention = AttentionPool(hidden_dim=lstm_cfg.hidden_size * 2)
        self.classifier = nn.Sequential(
            nn.Linear(lstm_cfg.hidden_size * 2, lstm_cfg.hidden_size),
            nn.ReLU(),
            nn.Dropout(lstm_cfg.dropout),
            nn.Linear(lstm_cfg.hidden_size, num_classes),
        )

    def forward(self, inputs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        # inputs shape: (batch, channels, sequence_length)
        x = self.cnn(inputs)
        x = x.transpose(1, 2)  # (batch, seq, features)
        outputs, _ = self.lstm(x)
        context, attention_weights = self.attention(outputs)
        logits = self.classifier(context)
        return logits, attention_weights


__all__ = [
    "CNNConfig",
    "BiLSTMConfig",
    "CNNBiLSTMAttention",
    "AttentionPool",
]
