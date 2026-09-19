# Dataset Research — Phase 1

This document records candidate datasets for Vietnamese Sign Language (VSL) and a short evaluation. Per project rules, no dataset was downloaded or integrated during this research.

## Candidates evaluated

### 1) VSL400 (Zenodo)
- Dataset name: VSL400 — A Multi-view Dataset for Vietnamese Word-Level Sign Language Recognition
- Source / URL: https://zenodo.org/records/17943574 (DOI: 10.5281/zenodo.17943574)
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Number of classes/signs: 400 glosses
- Number of samples/videos/images: 74,259 annotated video clips (total ≈ 53.99 hours)
- Data format: Synchronized multi-view RGB video files, JSON metadata (gloss labels, signer info). Preprocessed front/left/right view directories.
- Video or images: Video (multi-view RGB clips)
- Temporal/dynamic signs: Yes — word-level dynamic signs (isolated gloss instances), average duration ≈ 2.61s
- Signer/person info: Yes — 28 signers; signer IDs present in metadata; facial regions de-identified
- Train/validation/test splits: Metadata indicates signer-based splits (train/test with unseen signers) and single-view/multi-view evaluation possibilities; files restricted behind data usage agreement
- Suitable for real-time recognition: Technically yes (isolated word clips, single-view front camera available), suitable for model development and evaluation for word-level recognition
- Main limitations: Dataset files are access-restricted (requires agreeing to Data Usage Agreement); facial regions were de-identified (may limit facial cues); large size; intended for isolated word recognition not continuous-sentence recognition

Notes: Zenodo record marks the dataset as "restricted" for file download (public metadata available). See linked Data Usage Agreement: https://zenodo.org/records/21366957

### 2) VSL - Vietnamese Sign Language (Cropped) (Kaggle)
- Dataset name: VSL - Vietnamese Sign Language (Cropped)
- Source / URL: https://www.kaggle.com/datasets/nguyenanfms/vsl-vietnamese-sign-language-v2
- License: Listed as CC BY 4.0 (Kaggle page shows Attribution 4.0 International)
- Number of classes/signs: ~472 glosses (unified vocabulary after merging sources)
- Number of samples/videos/images: Processed corpus: ~26k raw clips in canonical set; processed/augmented sets reported (total repo ≈ 191k files; raw ~72 GB, processed ≈ 10 GB)
- Data format: `.mp4` front-view clips, `.npy` MediaPipe/3D skeleton keypoints, JSON labeling files, stratified split manifests
- Video or images: Video (cropped front-view) + extracted keypoints (`.npy`)
- Temporal/dynamic signs: Yes — word-level dynamic clips, temporal sequences preserved; keypoints arrays shape `[T, 76, 3]` reported
- Signer/person info: Partial — original VSL400 signer IDs preserved for core portion; online-harvested videos may lack signer metadata
- Train/validation/test splits: Yes — stratified splitting described (by gloss and signer), canonical 80/20 splits and signer-unseen test from VSL400
- Suitable for real-time recognition: Yes — provides front-view cropped clips and extracted keypoints usable for realtime model prototypes
- Main limitations: Mixed provenance (VSL400 + internet-harvested) — online-sourced data may have variable quality and licensing; large size; augmentation/imputation applied (verify provenance per clip before publication)

### 3) "Vietnamese Sign Language" (Kaggle — smaller upload)
- Dataset name: Vietnamese Sign Language (user upload)
- Source / URL: https://www.kaggle.com/datasets/ngannguyen65/vietnamese-sign-language
- License: Not specified on page (Unknown) — must verify with dataset owner before use
- Number of classes/signs: Appears to contain per-letter clips (alphabet) and per-sign pairs; size ≈ 2,539 files (1.7 GB in UI)
- Data format: Video files / folder per-sign (as uploaded)
- Video or images: Video (likely front-view clips and left/right splits visible in filenames)
- Temporal/dynamic signs: Yes (short clips), but vocabulary and annotation consistency unclear
- Signer/person info: Not clearly documented on Kaggle page
- Train/validation/test splits: Not explicitly provided
- Suitable for real-time recognition: Possibly for small-scale experiments (alphabet/limited classes), but licensing and provenance must be confirmed
- Main limitations: Unknown license, limited metadata, smaller scale, provenance unclear

### 4) GitHub projects & small datasets (notes)
- `trangphan10/VietNamese-Sign-Language` (GitHub): example project that simulates VSL using LSA64 (non-Vietnamese) to prototype models; uses LSA64 (Argentinian sign dataset) to mimic VSL. Not a native VSL dataset — unsuitable as direct VSL source.
- `raianrido/VSL` (GitHub): contains HamNoSys/SiGML dictionary and resources (GPL-3.0). Useful for avatar/animation mapping and dictionary resources, not for RGB video-based model training.
- `derricky2004/VSWD` (GitHub): VSWD — Vietnamese Sign Language Weather Dataset (small domain-specific dataset). Could be useful for domain-limited prototypes (weather vocabulary) but limited coverage.
- `thanhbinh55/Vietnamese-Sign-Language-Keypoint-Dataset` (GitHub): user-provided keypoint datasets and notebooks (small-scale; check license on repo). Useful as starter material but not a large benchmark.

## Comparison summary (candidate shortlist)

| Dataset | Source | License | Classes | Clips / Size | Video? | Temporal | Signer info | Splits | Suitable? | Main limitation |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| VSL400 | Zenodo (DOI) | CC BY 4.0 (files restricted; DUA) | 400 | 74,259 clips (~54 hr) | Yes (multi-view) | Yes | 28 signers (metadata) | Yes (signer-aware) | Highly suitable (research) | Controlled-access; DUA; large |
| VSL (Cropped) | Kaggle (nguyenanfms) | CC BY 4.0 | ~472 | Processed ~26k clips; raw ~72 GB | Yes (cropped front-view) + keypoints | Yes | Partial (VSL400 portion has signer IDs) | Yes (stratified) | Suitable (ready-for-prototyping) | Mixed provenance; verify licensing per online-sourced clips |
| Kaggle user uploads (various) | Kaggle (ngannguyen65, others) | Unknown/varies | small (alphabet or limited) | small (1–3 GB) | Yes | Yes | Often no metadata | No | Limited experiments | Unknown license; limited scale |
| GitHub resources (HamNoSys, SiGML, small datasets) | GitHub | Varies (GPL, MIT, etc.) | N/A or lexical resources | small | Not always video (SiGML is symbolic) | N/A | N/A or symbolic | N/A | Useful for dictionary/animation | Not direct RGB video training corpora |

## Recommendation (for further investigation)
- Primary candidate: **VSL400 (Zenodo)** — gold-standard multi-view, 400-class word-level VSL dataset with signer metadata and protocol for signer-unseen evaluation. Licensing is CC BY 4.0 but file access is controlled; obtain the Data Usage Agreement before downloading.
- Secondary candidate (practical): **VSL (Cropped) — Kaggle** — processed front-view + keypoints built from VSL400 and web sources. Useful for rapid prototyping (provides `.npy` keypoints) but verify the provenance and licensing of internet-harvested clips before publication or distribution.

## Licensing & data-quality concerns
- Zenodo VSL400: CC BY 4.0 for the dataset metadata and record; dataset files are access-restricted and require agreeing to a Data Usage Agreement due to residual biometric content — follow the DUA and cite the DOI. Verify any restrictions on redistribution.
- Kaggle VSL (Cropped): Kaggle page lists CC BY 4.0; still verify individual raw-source licenses for online-harvested clips if you intend to redistribute processed sets or publish derivatives.
- Many small user uploads on GitHub/Kaggle lack clear licensing or metadata — treat them as research-only until license is confirmed.

## If no suitable public VSL dataset existed
(Not applicable — VSL400 exists). If VSL400 had not been available, recommended MVP data-collection strategy for 20–30 classes:

1. Define 20–30 target glosses (high-frequency words/phrases) and canonical signer instructions.
2. Recruit 6–10 signers (balanced gender/age) and record multi-view front-only if multi-view not possible.
3. Record 30–50 repetitions per signer per gloss at 30 FPS, controlled backgrounds and some variation in lighting/distance.
4. Store raw video, per-frame timestamps, and per-clip JSON metadata (gloss, signer ID, recording conditions).
5. Extract and save MediaPipe/OpenPose keypoints as `.npy` for rapid model iteration; ensure same preprocessing during training/inference.
6. Create signer-held-out splits (train/val/test) to measure generalization to unseen signers.
7. Write and require a simple license and consent form covering research use and redistribution (or not) and anonymization (face blur) as needed.

## Files added/updated
- `docs/DATASET_RESEARCH.md` (this file)

---
End of Phase 1 research document. Do not download or integrate datasets until explicit approval.

## VSL400 — Phase 1 Feasibility Check (access & subset)

This section inspects the official VSL400 Zenodo record and the Data Usage Agreement to answer feasibility questions before any download.

1) How access to the video files is requested
- The VSL400 Zenodo record (DOI: 10.5281/zenodo.17943574) marks the dataset files as "restricted". The record states users must follow the access-request procedure described on the record page and review/submit the VSL400 Data Usage Agreement (DOI: 10.5281/zenodo.21366957).
- Practically: log in to Zenodo, open the VSL400 record, download and sign the `VSL400_Data_Usage_Agreement.pdf`, and submit the requested access form or contact the dataset maintainers. The record lists a contact person: Matej Šindelář (matej.sindelar@vsb.cz). Access to restricted files is granted only after completing the stated procedure.

2) What the Data Usage Agreement requires (high-level)
- The DUA is a controlled-access agreement (PDF on Zenodo). The Zenodo landing page instructs that users must review, complete and submit the DUA to obtain access.
- Typical DUA provisions (as signalled by the controlled-access decision on Zenodo): permitted use for academic/research, citation requirements, prohibition on attempts to re-identify participants, limitation on public redistribution of raw video, requirement to follow anonymization/handling rules, and to comply with local laws and the agreement terms. (I could not extract the PDF text programmatically; please review `https://zenodo.org/records/21366957` or the `VSL400_Data_Usage_Agreement.pdf` directly for exact clauses before signing.)

3) Whether metadata/annotations can be accessed without downloading full video archive
- The Zenodo record exposes summary metadata (counts, number of clips, views, that JSON metadata exists). However, the record states the dataset files are restricted; it is likely that per-clip JSON metadata files are included in the restricted files bundle and therefore require approval to download.
- Recommendation: request access and ask the maintainers whether they can provide (a) the per-clip metadata/label list only, or (b) a small manifest (gloss list + per-gloss clip counts and signer IDs) before granting full video download. Many controlled-access datasets allow sharing of non-sensitive metadata without full video access.

4) Whether we can identify/select ~20–30 glosses for our MVP
- Yes — VSL400 contains 400 glosses. The dataset structure includes JSON metadata with gloss labels and clip identifiers so selecting 20–30 glosses is technically straightforward once you have access to the label list or manifest.
- If access is delayed, ask the maintainers to provide a public label-list and per-gloss counts (or provide the list in the DUA response). The Kaggle processed derivative already demonstrates that a usable front-view subset and label lists can be assembled.

5) Whether the dataset provides signer IDs and gloss labels for signer-independent splits
- Yes — the Zenodo record explicitly states signer IDs are present in the JSON metadata (28 signers). The authors report signer-aware splits and mention signer-unseen test partitions. This supports creating signer-independent train/val/test splits.

6) Whether front-view videos alone are sufficient for our first prototype
- Yes — the dataset includes synchronized `front_view` recordings and the authors note single-view learning is supported. For an initial MVP (20–30 glosses, real-time prototype) front-view clips are sufficient and recommended (simpler processing, single-camera inference, aligns with many existing SLR baselines).

7) Estimate of amount of data needed if using only 20–30 classes and only front view
- Dataset totals: 74,259 clips across 400 glosses → mean ≈ 185.6 clips/gloss; average duration ≈ 2.61 s.
- Estimated clips for 20 glosses: ~3,712 clips → total duration ≈ 3,712 * 2.61 s ≈ 9,691 s ≈ 2.7 hours.
- Estimated clips for 30 glosses: ~5,568 clips → total duration ≈ 4.03 hours.
- Storage (front-view only) — compressed video estimate ranges (depends on resolution/codec):
	- Low estimate (~0.5 MB per clip): 20 classes → ~1.9 GB; 30 classes → ~2.8 GB.
	- Mid estimate (~1 MB per clip): 20 classes → ~3.7 GB; 30 classes → ~5.6 GB.
	- High estimate (~2 MB per clip): 20 classes → ~7.4 GB; 30 classes → ~11.1 GB.
- Practical expectation: plan for ~2–8 GB for the front-view video subset depending on chosen quality/resolution and container — storing extracted keypoints instead of video reduces size dramatically (tens to hundreds of MBs instead of GBs).

8) Whether downloading only a subset is technically possible (or controlled-access requires full archive)
- Zenodo controlled-access can be applied at file-level; after access is granted you typically can download individual files via the Zenodo UI or API. However, the dataset authors may have uploaded the files as grouped archives — in that case selective download may be less convenient.
- Recommendation: when requesting access, explicitly ask for selective access to `front_view` directories or for a manifest (gloss list + per-clip URLs) and whether maintainers can provide a curated small-subset (20–30 glosses) to speed prototyping. If maintainers packaged a single big archive, ask if they will provide a smaller subset upon request (many authors accommodate this for prototyping).

9) Official preprocessing / reference-code repository
- The Zenodo record mentions a consistent preprocessing pipeline but does not include a clearly linked public code repository on the record page. A public, official preprocessing repository was not found during a web search of the authors' names and the dataset name.
- Practical alternatives:
	- The Kaggle processed derivative (`vsl-vietnamese-sign-language-v2`) includes preprocessing notebooks and extracted `.npy` keypoints which can be reused (verify license/provenance first).
	- Contact the dataset authors (contact: Matej Šindelář) to request the official preprocessing scripts or reference evaluation code (recommended when requesting DUA access).

### Short actionable checklist (what to request from maintainers)
1. Submit the VSL400 Data Usage Agreement per Zenodo instructions (DOI: 10.5281/zenodo.21366957) and request access.
2. Ask maintainers to provide a non-sensitive manifest before approving full-download: label list (400 glosses), per-gloss counts, and signer ID mapping. This manifest should be shareable and is usually safe to publish.
3. Request a curated front-view subset (20–30 candidate glosses with signer-balanced clips) for prototyping — ask whether maintainers can provide it or whether we must download and filter locally.
4. Request the official preprocessing scripts or guidance (frame rate, resolution, crop, keypoint extraction parameters) to ensure training/inference parity.

---
Updated with VSL400 feasibility findings. Do not download videos or derivatives until DUA is signed and maintainers approve subset access.

## Current Status
Status:
- Dataset identified: VSL400
- Access: restricted
- DUA: required
- Full dataset download: NOT approved / NOT attempted
- Phase 2: BLOCKED pending access clarification
- Next action: manually review the email draft and submit the access request if appropriate

