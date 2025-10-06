from __future__ import annotations

from pathlib import Path

import numpy as np
import torch

from app.models.architecture import CNNBiLSTMAttention
from app.models.datasets import LightCurveDataset, SampleRecord
from app.models.losses import PhysicsInformedLoss


def test_dataset_pad_and_stack(tmp_path: Path):
    flux = np.random.rand(100).astype(np.float32)
    time = np.linspace(0, 1, 100).astype(np.float32)
    flux_path = tmp_path / "sample_flux.npy"
    time_path = tmp_path / "sample_time.npy"
    np.save(flux_path, flux)
    np.save(time_path, time)

    record = SampleRecord(flux_path=flux_path, time_path=time_path, label=1)
    dataset = LightCurveDataset([record], sequence_length=120)
    sample = dataset[0]
    inputs = sample["inputs"]
    assert inputs.shape == (2, 120)
    assert torch.allclose(inputs[1, 10:110], torch.from_numpy(flux))


def test_architecture_output_shape():
    model = CNNBiLSTMAttention(num_classes=3)
    inputs = torch.randn(4, 2, 256)
    logits, attention = model(inputs)
    assert logits.shape == (4, 3)
    assert attention.shape[0] == 4


def test_physics_loss_zero_when_matching():
    flux = torch.ones(2, 10)
    expected_depth = torch.zeros(2)
    loss_fn = PhysicsInformedLoss()
    loss = loss_fn(flux, expected_depth)
    assert torch.isclose(loss, torch.tensor(0.0))
