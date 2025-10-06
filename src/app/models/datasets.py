"""Datasets and data modules for light-curve training."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

try:  # Optional dependency – training module enables it when installed
    from pytorch_lightning import LightningDataModule
except ImportError:  # pragma: no cover
    LightningDataModule = object  # type: ignore


@dataclass(slots=True)
class SampleRecord:
    """Represents a preprocessed light-curve sample on disk."""

    flux_path: Path
    time_path: Path
    label: int
    metadata_path: Path | None = None

    @classmethod
    def from_npz(cls, path: Path, label: int) -> "SampleRecord":
        base = path.with_suffix("")
        return cls(flux_path=path, time_path=path, label=label, metadata_path=base.with_suffix(".json"))


def _load_array(path: Path) -> np.ndarray:
    if path.suffix == ".npz":
        data = np.load(path)
        if "flux" in data:
            return data["flux"]
        if "time" in data:
            return data["time"]
        raise KeyError(f"No suitable array in {path}")
    elif path.suffix == ".npy":
        return np.load(path)
    else:  # pragma: no cover - caller ensures extension
        raise ValueError(f"Unsupported file extension: {path.suffix}")


class LightCurveDataset(Dataset):
    """PyTorch dataset for prepared light curve tensors."""

    def __init__(
        self,
        samples: Sequence[SampleRecord],
        *,
        sequence_length: int = 2000,
        transform: Callable[[torch.Tensor], torch.Tensor] | None = None,
    ) -> None:
        self.samples = list(samples)
        self.sequence_length = sequence_length
        self.transform = transform

    def __len__(self) -> int:
        return len(self.samples)

    def _pad_or_crop(self, array: np.ndarray) -> np.ndarray:
        if array.ndim != 1:
            raise ValueError("Flux/time arrays must be 1D")
        target = self.sequence_length
        if array.size == target:
            return array
        if array.size > target:
            start = (array.size - target) // 2
            return array[start : start + target]
        pad_total = target - array.size
        pad_left = pad_total // 2
        pad_right = pad_total - pad_left
        return np.pad(array, (pad_left, pad_right), mode="constant", constant_values=0.0)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        record = self.samples[idx]
        flux = _load_array(record.flux_path)
        time = _load_array(record.time_path)
        flux = self._pad_or_crop(flux).astype(np.float32)
        time = self._pad_or_crop(time).astype(np.float32)

        x = torch.stack((torch.from_numpy(time), torch.from_numpy(flux)))

        if self.transform:
            x = self.transform(x)

        y = torch.tensor(record.label, dtype=torch.long)
        sample = {"inputs": x, "label": y}

        if record.metadata_path and record.metadata_path.exists():
            try:
                sample["metadata"] = json.loads(record.metadata_path.read_text())
            except json.JSONDecodeError:  # pragma: no cover
                sample["metadata"] = {}

        return sample


class LightCurveDataModule(LightningDataModule):
    """LightningDataModule orchestrating train/val/test splits for light curves."""

    def __init__(
        self,
        train_records: Sequence[SampleRecord],
        val_records: Sequence[SampleRecord],
        test_records: Sequence[SampleRecord] | None = None,
        *,
        batch_size: int = 32,
        num_workers: int = 4,
        sequence_length: int = 2000,
        transform: Callable[[torch.Tensor], torch.Tensor] | None = None,
    ) -> None:
        super().__init__()
        self.train_records = train_records
        self.val_records = val_records
        self.test_records = test_records or []
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.sequence_length = sequence_length
        self.transform = transform

    def setup(self, stage: str | None = None) -> None:
        self.train_dataset = LightCurveDataset(
            self.train_records,
            sequence_length=self.sequence_length,
            transform=self.transform,
        )
        self.val_dataset = LightCurveDataset(
            self.val_records,
            sequence_length=self.sequence_length,
            transform=self.transform,
        )
        self.test_dataset = LightCurveDataset(
            self.test_records,
            sequence_length=self.sequence_length,
            transform=self.transform,
        ) if self.test_records else None

    def train_dataloader(self) -> DataLoader:
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=True,
        )

    def val_dataloader(self) -> DataLoader:
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
        )

    def test_dataloader(self) -> DataLoader:
        if self.test_dataset is None:
            raise RuntimeError("Test dataset not configured")
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=True,
        )


__all__ = [
    "SampleRecord",
    "LightCurveDataset",
    "LightCurveDataModule",
]
