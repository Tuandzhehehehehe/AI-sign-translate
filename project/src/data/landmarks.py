"""Landmark extraction pipeline for Phase 2.

Provides a MediaPipe-backed LandmarkExtractor with an optional fake mode
for deterministic testing without any external video or dataset.

The extractor reads a video, processes frames, extracts hand (and optionally
pose) landmarks, and returns a numpy feature array and a detection mask.
"""
from typing import List, Optional, Tuple
import numpy as np
import cv2

try:
    import mediapipe as mp
except Exception:
    mp = None


class LandmarkExtractor:
    def __init__(self,
                 landmark_types: List[str] = ("hands",),
                 seq_len: Optional[int] = None,
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5,
                 use_fake: bool = False):
        """Create an extractor.

        Args:
            landmark_types: list containing any of 'hands' or 'pose'.
            seq_len: optional fixed output sequence length (None -> variable).
            min_detection_confidence: mediapipe detection threshold.
            min_tracking_confidence: mediapipe tracking threshold.
            use_fake: if True, do not call MediaPipe; generate deterministic synthetic landmarks.
        """
        self.landmark_types = landmark_types
        self.seq_len = seq_len
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.use_fake = use_fake

        # constants
        # hands: 21 landmarks per hand, each (x,y,z)
        self._hands_n = 21
        # pose: 33 landmarks
        self._pose_n = 33

        if not self.use_fake and mp is None:
            raise RuntimeError("mediapipe is required when use_fake=False")

    def _feature_dim(self) -> int:
        dim = 0
        if "hands" in self.landmark_types:
            # left + right hand, x,y,z each
            dim += self._hands_n * 2 * 3
        if "pose" in self.landmark_types:
            dim += self._pose_n * 3
        return dim

    def _process_frame_mediapipe(self, image: np.ndarray):
        mp_hands = mp.solutions.hands
        mp_pose = mp.solutions.pose

        # Initialize processors lazily per call for clarity (small overhead)
        hands = mp_hands.Hands(static_image_mode=False,
                               max_num_hands=2,
                               min_detection_confidence=self.min_detection_confidence,
                               min_tracking_confidence=self.min_tracking_confidence)
        pose = mp_pose.Pose(static_image_mode=False,
                             min_detection_confidence=self.min_detection_confidence,
                             min_tracking_confidence=self.min_tracking_confidence)

        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hand_res = hands.process(img_rgb)
        pose_res = pose.process(img_rgb)

        hands_landmarks = {"left": None, "right": None}
        if hand_res.multi_handedness and hand_res.multi_hand_landmarks:
            for idx, lm in enumerate(hand_res.multi_hand_landmarks):
                label = hand_res.multi_handedness[idx].classification[0].label.lower()
                arr = np.array([[p.x, p.y, p.z] for p in lm.landmark], dtype=np.float32)
                hands_landmarks[label] = arr

        pose_landmarks = None
        if pose_res.pose_landmarks:
            pose_landmarks = np.array([[p.x, p.y, p.z] for p in pose_res.pose_landmarks.landmark], dtype=np.float32)

        hands.close()
        pose.close()

        return hands_landmarks, pose_landmarks

    def _process_frame_fake(self, frame_idx: int, image_shape: Tuple[int,int]):
        # deterministic synthetic landmarks for tests
        h, w = image_shape
        # create simple circular trajectories
        t = frame_idx / max(1, (self.seq_len or 30))
        hands_landmarks = {"left": None, "right": None}
        if "hands" in self.landmark_types:
            base = np.linspace(0, 1, self._hands_n)[:, None]
            left = np.concatenate([base, base * 0 + 0.2, base * 0 + 0.1], axis=1)
            right = np.concatenate([base, base * 0 + 0.8, base * 0 + -0.1], axis=1)
            # shift slightly by t to simulate motion
            left[:, 0] = (left[:, 0] + 0.1 * np.sin(2 * np.pi * t))
            right[:, 0] = (right[:, 0] + 0.1 * np.cos(2 * np.pi * t))
            hands_landmarks["left"] = left.astype(np.float32)
            hands_landmarks["right"] = right.astype(np.float32)
        pose_landmarks = None
        if "pose" in self.landmark_types:
            base = np.linspace(0, 1, self._pose_n)[:, None]
            pose = np.concatenate([base, base * 0 + 0.5, base * 0 + 0.0], axis=1)
            pose[:, 0] += 0.05 * np.sin(2 * np.pi * t)
            pose_landmarks = pose.astype(np.float32)
        return hands_landmarks, pose_landmarks

    def extract_from_video(self, input_path: str, output_path: Optional[str] = None,
                           save_numpy: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """Extract landmarks from a video file.

        Returns (features, mask) where features is shape (T, D) and mask is bool (T,)
        indicating whether landmarks were detected for that frame.
        """
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"could not open video: {input_path}")

        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        features = []
        mask = []
        feat_dim = self._feature_dim()

        idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if self.use_fake:
                hands_landmarks, pose_landmarks = self._process_frame_fake(idx, frame.shape[:2])
            else:
                hands_landmarks, pose_landmarks = self._process_frame_mediapipe(frame)

            frame_feat = np.zeros((feat_dim,), dtype=np.float32)
            detected = False
            pos = 0
            if "hands" in self.landmark_types:
                # left then right, each 21x3
                for side in ("left", "right"):
                    lm = hands_landmarks.get(side)
                    if lm is not None:
                        detected = True
                        flat = lm.reshape(-1)
                        frame_feat[pos:pos + flat.size] = flat
                    pos += self._hands_n * 3
            if "pose" in self.landmark_types:
                if pose_landmarks is not None:
                    detected = True
                    flat = pose_landmarks.reshape(-1)
                    frame_feat[pos:pos + flat.size] = flat
                pos += self._pose_n * 3

            features.append(frame_feat)
            mask.append(bool(detected))
            idx += 1

        cap.release()

        features = np.stack(features, axis=0) if features else np.zeros((0, feat_dim), dtype=np.float32)
        mask = np.array(mask, dtype=bool)

        # apply seq_len padding/truncation if requested
        if self.seq_len is not None:
            from .preprocessing import pad_or_truncate
            features = pad_or_truncate(features, self.seq_len)
            mask = pad_or_truncate(mask.astype(np.int32), self.seq_len).astype(bool)

        if save_numpy and output_path:
            np.savez_compressed(output_path, features=features, mask=mask)

        return features, mask
