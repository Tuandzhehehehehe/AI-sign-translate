import numpy as np
import torch

from src.models.lstm import SequenceLSTMClassifier
from src.models.gru import SequenceGRUClassifier


def test_lstm_forward_pass_and_loss():
    batch_size = 2
    seq_len = 8
    input_size = 126
    num_classes = 5

    x = torch.randn(batch_size, seq_len, input_size)
    y = torch.randint(0, num_classes, (batch_size,))
    model = SequenceLSTMClassifier(input_size=input_size, hidden_size=16, num_layers=2, num_classes=num_classes)
    logits = model(x)
    assert logits.shape == (batch_size, num_classes)

    loss_fn = torch.nn.CrossEntropyLoss()
    loss = loss_fn(logits, y)
    assert torch.isfinite(loss)


def test_gru_forward_pass_and_loss():
    batch_size = 3
    seq_len = 10
    input_size = 126
    num_classes = 7

    x = torch.randn(batch_size, seq_len, input_size)
    y = torch.randint(0, num_classes, (batch_size,))
    model = SequenceGRUClassifier(input_size=input_size, hidden_size=12, num_layers=2, num_classes=num_classes)
    logits = model(x)
    assert logits.shape == (batch_size, num_classes)

    loss_fn = torch.nn.CrossEntropyLoss()
    loss = loss_fn(logits, y)
    assert torch.isfinite(loss)


def test_one_step_training_loop_runs():
    model = SequenceLSTMClassifier(input_size=126, hidden_size=8, num_layers=1, num_classes=4)
    x = torch.randn(2, 8, 126)
    y = torch.randint(0, 4, (2,))

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = torch.nn.CrossEntropyLoss()

    optimizer.zero_grad()
    logits = model(x)
    loss = criterion(logits, y)
    loss.backward()
    optimizer.step()

    assert torch.isfinite(loss)
