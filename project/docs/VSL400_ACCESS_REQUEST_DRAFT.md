To: Matej Šindelář <matej.sindelar@vsb.cz>
Subject: Access request for VSL400 dataset — university graduation project (Phase 1 inquiry)

Dear Dr. Šindelář,

I hope this message finds you well. I am a university student developing a graduation project on real-time Vietnamese Sign Language (VSL) recognition using computer vision and deep learning. Our work will follow the VSL400 dataset paper and build a small prototype for isolated word-level recognition.

Project summary (planned prototype):
- Dataset: VSL400 (multi-view word-level dataset)
- Goal: prototype real-time recognition for approximately 20–30 isolated gloss classes
- Modality: front-view videos only
- Processing: MediaPipe landmark/keypoint extraction
- Model: LSTM/GRU baseline for sequence classification
- Evaluation: signer-independent train/validation/test split
- Deployment target: real-time webcam inference for a demonstration

We respectfully request guidance on accessing the VSL400 dataset and compliance with the Data Usage Agreement. Specifically, could you please let us know:

1. Is a student/university graduation project eligible to request access to the VSL400 video files under the current Data Usage Agreement terms?
2. What is the proper procedure to submit the DUA / access request? Should we sign and upload the DUA PDF via Zenodo, or is email contact preferred?
3. For prototyping, would it be possible to request a limited access subset (approximately 20–30 glosses) rather than downloading the entire dataset? If so, what is the preferred way to request such a subset?
4. Can you provide a public/non-sensitive manifest (or allow us to access one) containing:
   - the list of gloss labels,
   - the number of clips available per gloss,
   - signer ID mapping for each clip,
   - any existing train/validation/test split information (or recommended signer-unseen split)
   This manifest would enable us to select a balanced MVP subset without immediate access to the full videos.
5. Are the `front_view` files available independently (i.e., can we request only the front camera recordings)?
6. Is there an official preprocessing/reference-code repository available (frame extraction, alignment, keypoint extraction settings, or evaluation scripts) that we may reuse for consistent preprocessing and evaluation?
7. Do you provide an official recommended train/validation/test split for signer-independent evaluation? If not, can you recommend a signer-split strategy consistent with prior evaluations on VSL400?
8. After processing authorized videos, are we permitted to store and use extracted MediaPipe keypoints (`.npy` files) as derivative data for our internal experiments and prototype, subject to the DUA terms?
9. Are there any specific citation, redistribution, storage, deletion, or publication requirements we should be aware of when using VSL400 for a student project and a demonstration prototype?

We will not publish or redistribute raw video files; our intention is to follow the DUA and any additional guidance you provide. If you prefer, we can provide a short project description and our institutional affiliation for record-keeping.

Thank you for your time and for creating this important dataset. We appreciate any guidance you can provide.

Sincerely,

[Your Name]
[University / Department]
[Email]
[Optional: Supervisor / Advisor name]
