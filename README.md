# Real-Time Vietnamese Sign Language to Text

## Tổng quan

Đây là dự án đồ án tốt nghiệp xây dựng hệ thống nhận dạng ngôn ngữ ký hiệu tiếng Việt (Vietnamese Sign Language - VSL) theo thời gian thực từ webcam, chuyển đổi sang văn bản tiếng Việt và chuẩn bị cho mô hình phân loại chuỗi cử động tay/thân.

Mục tiêu của dự án là xây dựng một pipeline rõ ràng, có thể kiểm chứng theo từng giai đoạn:

- thu thập/đọc frame từ webcam;
- trích xuất landmark bằng MediaPipe;
- chuẩn hóa và tạo chuỗi thời gian có độ dài cố định;
- huấn luyện mô hình LSTM/GRU trên dữ liệu landmark;
- dự đoán ký hiệu và hiển thị kết quả dạng văn bản.

Dự án hiện đang ở trạng thái kiểm tra kiến trúc và chốt dữ liệu theo đúng từng pha, không đi quá xa khỏi phạm vi đã được phê duyệt.

---

## Mục tiêu đồ án

- Xây dựng hệ thống nhận diện ký hiệu VSL theo thời gian thực.
- Ưu tiên MVP với khoảng 20–30 lớp ký hiệu.
- Dùng dữ liệu landmark thay vì ảnh thô làm đầu vào cho mô hình.
- Giữ class names, đường dẫn dữ liệu và cấu hình mô hình ở dạng có thể cấu hình.
- Tập trung vào một pipeline ổn định, có thể chạy được trên CPU trong giai đoạn thử nghiệm.
- Không giả định hoặc tự ý tích hợp dataset bên ngoài nếu chưa được phê duyệt.

---

## Kiến trúc mục tiêu

Pipeline mục tiêu:

Webcam
→ OpenCV frame capture
→ MediaPipe hand/pose landmark extraction
→ preprocessing sequence
→ model classifier (LSTM/GRU)
→ confidence filtering
→ recognized sign
→ Vietnamese text output

---

## Công nghệ sử dụng

- C++17 / CMake (hệ thống build và giao diện UI)
- SDL3 (quản lý cửa sổ, renderer và camera/webcam subsystem)
- Python 3.x
- OpenCV
- MediaPipe
- PyTorch
- NumPy
- pytest
- cấu hình YAML

---

## Trạng thái hiện tại của dự án

### Phase 0
- Hoàn thành.
- Đã chuẩn bị repo, cấu trúc thư mục, config mẫu, requirements và folder cho dữ liệu, mô hình, checkpoint, output.

### Phase 1
- Nghiên cứu và đánh giá dataset đã được thực hiện.
- Các ứng viên hiện tại gồm:
  - VSL400 (Zenodo)
  - VSL - Cropped (Kaggle)
- Dữ liệu đang ở trạng thái nghiên cứu, chưa được tải xuống hoặc tích hợp vào dự án.
- Cửa ngõ phê duyệt dataset vẫn đang hoạt động: dữ liệu chỉ được dùng sau khi đã xác nhận quyền sử dụng, provenance, license và tính phù hợp với mục tiêu đồ án.

### Phase 2
- Đã xác thực pipeline trích xuất landmark và preprocessing.
- Pipeline sử dụng MediaPipe cho hand landmarks, có hỗ trợ pose landmarks nếu cần.
- Có cơ chế xử lý missing detections bằng zero-filled vectors và mask boolean.
- Hỗ trợ chuỗi có độ dài cố định thông qua padding/truncation.
- Có kiểm thử synthetic và đã chạy thành công.

### Phase 3
- Đã chuẩn bị kiến trúc mô hình LSTM/GRU sơ bộ và các test synthetic.
- Mô hình nhận đầu vào là landmark sequence, không phải ảnh gốc.
- Chưa tích hợp dataset thực, chưa bắt đầu training trên dữ liệu thực.

> Lưu ý quan trọng: Dự án hiện đang ở trạng thái “đã xác minh kiến trúc, nhưng chưa vượt qua cổng phê duyệt dữ liệu”.

---

## Cấu trúc repo

```text
project/
├── BUILD_PLAN.md
├── README.md
├── requirements.txt
├── configs/
│   └── config.yaml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── DATASET_RESEARCH.md
│   ├── PHASE_2_LANDMARK_PIPELINE.md
│   └── VSL400_ACCESS_REQUEST_DRAFT.md
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── landmarks.py
│   │   └── preprocessing.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── lstm.py
│   │   └── gru.py
│   ├── training/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   └── evaluate.py
│   ├── inference/
│   └── utils/
├── checkpoints/
├── outputs/
├── tests/
│   ├── test_landmarks.py
│   └── test_models.py
└── .venv/
```

---

## Phase 2: landmark extraction pipeline

### Mục tiêu

Pipeline của Phase 2 phục vụ cho bước chuẩn bị dữ liệu đầu vào cho mô hình thời gian, với yêu cầu:

- đọc video cục bộ bằng OpenCV;
- duyệt frame theo thứ tự;
- trích xuất landmark tay; pose là tùy chọn;
- chuẩn hóa tọa độ;
- xử lý trường hợp không detect được landmarks;
- tạo chuỗi có độ dài cố định nếu cần;
- lưu/trả về định dạng feature thống nhất.

### Định dạng feature hiện tại

Đối với cấu hình hand-only, feature dimension hiện tại là:

- 21 landmark/tay × 2 tay × 3 tọa độ = 126

Một chuỗi landmark sẽ có dạng:

- [T, 126] cho một sequence đơn
- [batch_size, T, 126] cho batch đầu vào cho mô hình

### Xử lý missing detection

Nếu frame không phát hiện được landmark, hệ thống sẽ:

- đặt vector landmark đó bằng 0;
- ghi nhận trạng thái missing trong mask boolean;
- không làm crash pipeline.

### Chuẩn hóa

Chuẩn hóa hiện tại được thực hiện bằng preprocessing utility, theo dạng per-frame normalization cơ bản:

- trừ mean của x/y trong từng frame;
- scale theo giá trị tuyệt đối lớn nhất để giảm độ lớn tọa độ.

---

## Phase 3: mô hình baseline

### Mô hình hỗ trợ

- LSTM classifier
- GRU classifier

### Input

Mô hình nhận đầu vào dạng sequence landmark:

```python
[batch_size, sequence_length, input_size]
```

Trong đó:

- `sequence_length`: độ dài chuỗi thời gian
- `input_size`: kích thước đặc trưng của một frame landmark

### Output

Mô hình trả về logits dạng:

```python
[batch_size, num_classes]
```

Class names và mapping được giữ bên ngoài mô hình để tránh hard-code tên lớp trong code.

---

## Quy tắc dữ liệu và dataset

### Cấm trong giai đoạn hiện tại

- không tải xuống dataset ngoài ý muốn;
- không tích hợp VSL400, VSL-Cropped hoặc dataset khác mà không được phê duyệt;
- không bắt đầu training trên dữ liệu thực;
- không tự tạo class names giả cho VSL;
- không khẳng định mô hình đã hoạt động trên tiếng ký hiệu Việt Nam thực tế.

### Cửa ngõ dữ liệu đang hoạt động

Dự án chỉ được tiến xa hơn khi có đủ thông tin về:

- license;
- provenance;
- labels/class mapping;
- định dạng video hoặc landmark;
- độ phù hợp với 20–30 lớp MVP;
- quyền sử dụng cho đồ án tốt nghiệp;
- tính hợp pháp và đạo đức của dữ liệu.

---

## Cài đặt và Thiết lập (Setup)

Hệ thống sử dụng **CMake** kết hợp **FetchContent** để tự động tải và cấu hình thư viện **SDL3**, đồng thời tự động tạo môi trường ảo Python (`.venv`) và cài đặt các phụ thuộc từ `requirements.txt`.

### 1. Cấu hình tự động bằng CMake

Từ thư mục gốc của dự án, chạy lệnh:

```bash
cmake -B build
```

Quá trình này tự động:
1. Tải và build SDL3 (`release-3.2.28`) từ kho lưu trữ chính thức.
2. Tạo môi trường ảo `.venv` nếu chưa có.
3. Chạy `pip install -r requirements.txt` để cài đặt đầy đủ phụ thuộc Python vào `.venv`.
4. Sinh file kích hoạt môi trường (`build/activate.sh` trên Linux/macOS hoặc `build/activate.bat` trên Windows).

### 2. Biên dịch ứng dụng UI

```bash
cmake --build build
```

---

## Kích hoạt môi trường ảo (Activate Environment)

Sau khi CMake hoàn tất cấu hình, bạn có thể kích hoạt môi trường ảo Python:

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  # hoặc dùng script sinh tự động trong build:
  source build/activate.sh
  ```

- **Windows (PowerShell):**
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  .\.venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt):**
  ```cmd
  call build\activate.bat
  ```

---

## Chạy ứng dụng (Run)

### 1. Chạy giao diện camera SDL3

Sau khi build thành công:

- **Linux / macOS:**
  ```bash
  ./build/ai_sign_translate_ui
  ```

- **Windows:**
  ```cmd
  .\build\Debug\ai_sign_translate_ui.exe
  # hoặc
  .\build\Release\ai_sign_translate_ui.exe
  ```

> **Lưu ý:** Ứng dụng sẽ tự động kết nối và hiển thị luồng video từ webcam của thiết bị. Nếu thiết bị không có webcam hoặc chưa cấp quyền truy cập camera, ứng dụng sẽ thông báo trên terminal và hiển thị hộp thoại cảnh báo.

### 2. Chạy kiểm thử (Test)

Chạy kiểm thử pipeline Python trong môi trường ảo:

- **Linux / macOS:**
  ```bash
  PYTHONPATH=. .venv/bin/python -m pytest -q tests/test_landmarks.py
  ```

- **Windows (sau khi kích hoạt môi trường):**
  ```powershell
  $env:PYTHONPATH="."
  python -m pytest -q tests/test_landmarks.py
  ```

---

## Dữ liệu và hướng đi tiếp

Hiện tại dự án đang ở trạng thái chuẩn bị kiến trúc và kiểm tra chốt yếu tố kỹ thuật trước khi tiếp tục với dataset thực.

Các bước tiếp theo sẽ là:

1. xác nhận dataset phù hợp và được phê duyệt;
2. xác minh format dữ liệu và class mapping;
3. chuẩn hóa pipeline training/inference dựa trên cùng một preprocessing;
4. tiến tới Phase 4 khi dataset đã được xác nhận.

---

## Lưu ý quan trọng

- Đây không phải là “mô hình nhận diện VSL đã hoạt động” trên dữ liệu thực tế.
- Hiện tại, mọi kết quả đã xác minh chỉ là kiến trúc và test synthetic.
- Mọi khẳng định về độ chính xác trên tiếng ký hiệu Việt Nam phải dựa trên dữ liệu thực đã được phê duyệt và đánh giá phù hợp.

---

## Kết luận

Đồ án này đang đi đúng hướng theo phương pháp pha hóa: từ nền tảng repo → nghiên cứu dataset → chuẩn bị preprocessing → xây dựng kiến trúc mô hình → chờ phê duyệt dữ liệu thực trước khi tiến vào training chính thức.

Mục tiêu hiện tại là có một pipeline rõ ràng, chuẩn hóa, kiểm thử được và sẵn sàng cho giai đoạn dataset-approved tiếp theo.
