"""Preprocessing utilities for landmark sequences.

Functions:
- normalize_landmarks: center and scale landmarks per-frame.
- pad_or_truncate: enforce fixed sequence length.
- to_tensor: convert numpy sequence -> torch tensor (if torch available) or numpy.
"""
from typing import Optional
import numpy as np


def normalize_landmarks(features: np.ndarray, method: str = "center_scale") -> np.ndarray:
    """Normalize per-frame landmarks.

    Args:
        features: array shape (T, D) where D is concatenated x,y,z values.
        method: currently only 'center_scale' supported.

    Returns:
        normalized features same shape as input.
    """
    if features.size == 0:
        return features

    if method == "center_scale":
        # reshape to (T, N, 3)
        T, D = features.shape
        if D % 3 != 0:
            raise ValueError("feature dimension must be multiple of 3")
        N = D // 3
        reshaped = features.reshape(T, N, 3)
        # center each frame by mean of available (x,y) ignoring zeros
        centered = np.empty_like(reshaped)
        for t in range(T):
            frame = reshaped[t]
            mean = frame[:, :2].mean(axis=0)
            frame[:, :2] = frame[:, :2] - mean
            # scale by max abs value to bring coordinates roughly in [-1,1]
            denom = np.abs(frame[:, :2]).max()
            if denom > 0:
                frame[:, :2] = frame[:, :2] / denom
            centered[t] = frame
        return centered.reshape(T, D)
    else:
        raise ValueError(f"unknown normalization method: {method}")


def pad_or_truncate(sequence: np.ndarray, length: int) -> np.ndarray:
    """Pad (with zeros) or truncate a sequence to `length` along axis 0.

    Works with 1D or 2D arrays. Preserves dtype.
    """
    if sequence.ndim == 1:
        seq_len = sequence.shape[0]
        if seq_len == length:
            return sequence
        if seq_len > length:
            return sequence[:length]
        pad = np.zeros((length - seq_len,), dtype=sequence.dtype)
        return np.concatenate([sequence, pad], axis=0)
    elif sequence.ndim == 2:
        seq_len = sequence.shape[0]
        feat_dim = sequence.shape[1]
        if seq_len == length:
            return sequence
        if seq_len > length:
            return sequence[:length, :]
        pad = np.zeros((length - seq_len, feat_dim), dtype=sequence.dtype)
        return np.vstack([sequence, pad])
    else:
        raise ValueError("sequence must be 1D or 2D numpy array")


def to_tensor(sequence: np.ndarray):
    """Convert to a torch tensor if torch is installed, otherwise return numpy.

    This function avoids importing torch at module import time.
    """
    try:
        import torch
    except Exception:
        return sequence
    return torch.from_numpy(sequence)
