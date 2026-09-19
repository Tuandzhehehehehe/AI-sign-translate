Phase 2 — Landmark Extraction Pipeline
=====================================

Overview
--------
This document describes the landmark extraction pipeline prepared in Phase 2.

Input
-----
- A local video file readable by OpenCV (any codec supported by the system's OpenCV build).
- The extractor is configurable to use `hands` and/or `pose` landmarks.

Frame processing
----------------
- Frames are read sequentially using OpenCV `VideoCapture` to preserve ordering.
- Each frame is passed to MediaPipe (unless `use_fake=True`), extracting:
  - `hands`: up to two hands, 21 landmarks each (x,y,z)
  - `pose`: 33 landmarks (x,y,z)
- Missing detections are tolerated: frames without detections are represented as zeroed feature vectors and flagged in a boolean mask.

Landmark representation
-----------------------
- Features are flattened per-frame into a single 1D vector: [left_hand(21x3), right_hand(21x3), pose(33x3)]
- Coordinates are MediaPipe's normalized coordinates (x,y in [0,1], z relative depth) when using real MediaPipe.

Missing detection handling
--------------------------
- If a hand/pose is not detected for a frame, corresponding slots in the flat vector are zeros.
- A boolean mask of length T indicates frames with at least one detection.

Normalization
-------------
- Per-frame center and scale normalization is provided in `normalize_landmarks`.
- Current default: subtract per-frame mean(x,y) then divide by per-frame max absolute value.

Sequence length
---------------
- The extractor supports an optional fixed `seq_len` parameter.
- If set, sequences shorter than `seq_len` are padded with zeros; longer sequences are truncated.

Output format
-------------
- Numpy array `features` shape (T, D) where D is the flattened landmark dimension.
- Boolean mask `mask` shape (T,) indicating frames with detected landmarks.
- Optionally saved as a compressed `.npz` archive containing `features` and `mask`.

Integration with LSTM/GRU
-------------------------
- After normalization and conversion to tensors, the data shape expected by sequence models is `(T, D)` or `(batch, T, D)` depending on the training pipeline.
- `to_tensor` utility converts numpy arrays to PyTorch tensors when `torch` is available.

Notes and constraints
---------------------
- This phase does not access or download any restricted datasets; use `use_fake=True` for local testing.
- Do not assume any dataset-specific file layout; the extractor operates on one video at a time.
