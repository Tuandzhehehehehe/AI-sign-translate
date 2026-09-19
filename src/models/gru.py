"""Baseline GRU sequence classifier for landmark inputs."""
from __future__ import annotations

from typing import Dict, Optional

import torch
from torch import nn


class SequenceGRUClassifier(nn.Module):
    def __init__(
        self,
        input_size: int,
        hidden_size: int = 64,
        num_layers: int = 2,
        dropout: float = 0.2,
        num_classes: int = 20,
        sequence_length: Optional[int] = None,
        bidirectional: bool = False,
    ) -> None:
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.num_classes = num_classes
        self.sequence_length = sequence_length
        self.bidirectional = bidirectional

        self.gru = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0.0,
            batch_first=True,
            bidirectional=bidirectional,
        )
        direction_factor = 2 if bidirectional else 1
        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(hidden_size * direction_factor, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() != 3:
            raise ValueError(f"expected input shape [batch, seq_len, input_size], got {tuple(x.shape)}")
        out, _ = self.gru(x)
        last_step = out[:, -1, :]
        return self.classifier(last_step)

    def get_config(self) -> Dict[str, object]:
        return {
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "num_layers": self.num_layers,
            "dropout": self.dropout,
            "num_classes": self.num_classes,
            "sequence_length": self.sequence_length,
            "bidirectional": self.bidirectional,
        }
