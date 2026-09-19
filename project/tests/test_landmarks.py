import numpy as np
from src.data.landmarks import LandmarkExtractor
from src.data import preprocessing


def test_fake_extractor_shapes_and_mask():
    # create a tiny synthetic video using OpenCV VideoWriter
    h, w = 64, 64
    fourcc = 0
    # produce frames in memory by writing to temporary file
    import tempfile, cv2

    tmp = tempfile.NamedTemporaryFile(suffix='.avi', delete=False)
    path = tmp.name
    tmp.close()
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'XVID'), 10.0, (w, h))
    for i in range(5):
        frame = (np.ones((h, w, 3), dtype=np.uint8) * (i * 20)).astype(np.uint8)
        out.write(frame)
    out.release()

    ext = LandmarkExtractor(landmark_types=['hands'], seq_len=8, use_fake=True)
    features, mask = ext.extract_from_video(path, save_numpy=False)

    # features should be (8, D) because seq_len pads to 8
    assert features.shape[0] == 8
    assert mask.shape[0] == 8
    # feature dim should be 21*2*3
    assert features.shape[1] == 21 * 2 * 3


def test_padding_and_truncation():
    seq = np.random.randn(3, 10).astype(np.float32)
    out = preprocessing.pad_or_truncate(seq, 5)
    assert out.shape == (5, 10)
    out2 = preprocessing.pad_or_truncate(seq, 2)
    assert out2.shape == (2, 10)


def test_normalization_no_crash():
    seq = np.random.rand(4, 21 * 2 * 3).astype(np.float32)
    norm = preprocessing.normalize_landmarks(seq)
    assert norm.shape == seq.shape


def test_to_tensor_returns_numpy_if_no_torch():
    import sys
    # Ensure torch not imported in this environment test; behavior is allowed either way
    seq = np.zeros((2, 3), dtype=np.float32)
    t = preprocessing.to_tensor(seq)
    # If torch is installed, ensure it's a tensor; otherwise numpy
    try:
        import torch
        assert hasattr(t, 'numpy')
    except Exception:
        assert isinstance(t, np.ndarray)
