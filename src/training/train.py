"""Training entry-point scaffold for future data-driven training.

This module is intentionally dataset-independent. It expects the caller to provide:
- dataset path or loader
- class mapping
- model instance
- training config
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import torch
from torch import nn
from torch.utils.data import DataLoader


@dataclass
class TrainingConfig:
    batch_size: int = 32
    learning_rate: float = 1e-3
    epochs: int = 10
    device: str = "cpu"
    seed: int = 42
    checkpoint_dir: str = "./checkpoints"


def set_seed(seed: int = 42) -> None:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: str = "cpu",
) -> float:
    model.train()
    total_loss = 0.0
    count = 0
    for batch in dataloader:
        inputs, labels = batch
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        count += 1
    return total_loss / max(1, count)
