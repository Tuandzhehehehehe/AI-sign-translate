"""Evaluation scaffold for future model validation."""
from __future__ import annotations

from typing import Iterable

import torch
from torch import nn


def evaluate(model: nn.Module, data_loader: Iterable, criterion: nn.Module, device: str = "cpu") -> float:
    model.eval()
    total_loss = 0.0
    count = 0
    with torch.no_grad():
        for batch in data_loader:
            inputs, labels = batch
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            count += 1
    return total_loss / max(1, count)
