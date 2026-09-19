# BUILD PLAN – REAL-TIME VIETNAMESE SIGN LANGUAGE TO TEXT

## 1. Project Goal
Build a real-time computer-vision system that uses a webcam to recognize Vietnamese sign-language gestures and convert them into Vietnamese text displayed on screen.

The first release must focus on a small, reliable vocabulary and a modular architecture that can later scale.

## 2. Target Pipeline
Webcam → OpenCV frame capture → MediaPipe hand/pose landmark extraction → sequence preprocessing → trained AI classifier → confidence filtering/smoothing → recognized sign → Vietnamese text display.

## 3. Initial MVP Scope
- Start with approximately 20–30 sign classes.
- Support real-time webcam inference.
- Show predicted Vietnamese word/phrase and confidence.
- Keep dataset, model, class list, and UI configurable.
- Prioritize a working end-to-end prototype before advanced features.

## 4. Recommended Stack
- Python 3.x
- OpenCV – webcam capture and real-time display
- MediaPipe – hand/pose landmark extraction
- PyTorch – model training and inference
- LSTM or GRU – temporal sequence classification
- NumPy / Pandas – data processing
- scikit-learn – evaluation metrics
- Matplotlib – training/evaluation visualization
- Optional later: FastAPI/Flask + HTML/CSS/JavaScript

## 5. Development Phases

### Phase 0 – Repository & Architecture
Create a clean project structure, requirements file, README, configuration, data/model/output directories, and a single configuration source for class names and hyperparameters.
**Deliverable:** project runs locally with documented setup.

### Phase 1 – Dataset
Select or create a dataset for the initial 20–30 sign classes. Record multiple people, backgrounds, lighting conditions, distances, and repetitions where possible. Separate train/validation/test by subject when feasible.
**Deliverable:** versioned dataset + class mapping + dataset statistics.

### Phase 2 – Landmark Extraction
Build preprocessing that extracts MediaPipe hand landmarks and optionally pose landmarks, normalizes coordinates, handles missing detections, and saves fixed-length sequences.
**Deliverable:** reusable landmark extraction pipeline + sample verification.

### Phase 3 – Baseline Model
Implement an LSTM or GRU sequence classifier. Input: sequence of normalized landmark vectors. Output: configured sign class.
**Deliverable:** trainable model + checkpoint + inference script.

### Phase 4 – Training & Evaluation
Track loss and accuracy. Report precision, recall, F1-score and confusion matrix. Check per-class performance.
**Deliverable:** metrics, plots, confusion matrix, best checkpoint.

### Phase 5 – Real-Time Inference
Connect webcam → MediaPipe → sequence buffer → model → prediction. Add confidence threshold and temporal smoothing/debouncing.
**Deliverable:** stable real-time demo.

### Phase 6 – Text Assembly
Convert recognized signs into a text stream. Avoid repeating the same prediction every frame. Add reset/clear.
**Deliverable:** readable Vietnamese text output.

### Phase 7 – UI
Show webcam feed, prediction, confidence, translated text, clear/reset control, and model status.
**Deliverable:** demo-ready interface.

### Phase 8 – Testing & Optimization
Measure FPS, latency, accuracy, robustness under lighting/background changes, and false predictions.
**Deliverable:** final test report.

### Phase 9 – Documentation
Document architecture, dataset, preprocessing, model, training, experiments, evaluation, limitations, and future work.
**Deliverable:** graduation-project documentation.

## 6. Suggested Project Structure
```text
sign-language-ai/
├── README.md
├── requirements.txt
├── configs/
│   └── config.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── classes.json
├── src/
│   ├── data/
│   │   ├── collect.py
│   │   ├── extract_landmarks.py
│   │   └── dataset.py
│   ├── models/
│   │   ├── lstm.py
│   │   └── gru.py
│   ├── training/
│   │   ├── train.py
│   │   └── evaluate.py
│   ├── inference/
│   │   └── realtime.py
│   └── utils/
│       ├── preprocessing.py
│       └── visualization.py
├── checkpoints/
├── outputs/
│   ├── metrics/
│   └── plots/
└── tests/
```

## 7. Functional Requirements
- FR-01: Capture webcam frames in real time.
- FR-02: Detect and extract relevant hand landmarks; support optional pose landmarks.
- FR-03: Normalize landmarks consistently between training and inference.
- FR-04: Maintain a temporal frame buffer for dynamic signs.
- FR-05: Predict a configured sign class and confidence.
- FR-06: Apply confidence thresholding and temporal smoothing.
- FR-07: Display recognized Vietnamese text.
- FR-08: Prevent duplicate text caused by repeated identical frames.
- FR-09: Provide clear/reset functionality.
- FR-10: Save/load trained model checkpoints.

## 8. Engineering Rules for the AI Agent
1. Implement one phase at a time. Do not skip phases.
2. Verify each phase before moving to the next.
3. Do not rewrite working code without a reason.
4. Before selecting a dataset, inspect license, labels, format, language/sign system, and suitability for Vietnamese Sign Language.
5. Never claim an ASL dataset is Vietnamese Sign Language. Document limitations clearly.
6. Keep class labels configurable and avoid hard-coding them in multiple files.
7. Use the same preprocessing implementation for training and inference.
8. Handle missing hand detections gracefully.
9. Keep CPU inference possible for the demo where practical.
10. Log important configuration, model version, dataset version, and evaluation results.
11. Every major module should have a small verification/test.
12. Never hide errors. Report the exact failing file, command, and likely cause.
13. Update README.md after each major phase.

## 9. Definition of Done – MVP
- Webcam opens successfully.
- MediaPipe detects required landmarks.
- A sequence is created from consecutive frames.
- A trained model loads successfully.
- Initial 20–30 classes can be predicted.
- Prediction and confidence are shown in real time.
- Temporal smoothing prevents excessive flickering.
- Recognized signs become readable Vietnamese text.
- Clear/reset works.
- Training and evaluation commands are documented.
- Test metrics and limitations are documented.

## 10. First Tasks for the AI Agent
1. Create the project skeleton and requirements.txt.
2. Verify Python/PyTorch/OpenCV/MediaPipe environment.
3. Research candidate Vietnamese Sign Language datasets and report license, number of classes, format, and suitability before integrating one.
4. If no suitable dataset exists for the selected MVP vocabulary, create a local webcam data-collection tool.
5. Implement landmark extraction and save a small sample dataset.
6. Visualize/inspect several processed samples.
7. Only then implement LSTM/GRU training.

## 11. Future Extensions
- Increase vocabulary to 50–100+ signs.
- Use both hands, body pose, and facial landmarks where required.
- Improve sentence segmentation/context handling.
- Add Vietnamese text-to-speech.
- Add speech/text-to-sign output.
- Explore Transformer-based temporal models if data/compute are sufficient.
- Package as desktop/web application.

## 12. Expected Final Demo
A user stands in front of a webcam and performs a supported Vietnamese sign. The system detects landmarks, processes a short sequence, predicts the sign, and displays the corresponding Vietnamese text in real time, with confidence and a clear/reset function.
