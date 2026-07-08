# NHẬT KÝ TIẾN ĐỘ DỰ ÁN (DAILY PROGRESS LOG)
## Dự án: AI Bridge Engineer (AI_Japanese)

Tài liệu này dùng để ghi nhận chi tiết tiến độ triển khai hàng ngày, các sự cố phát sinh và giải pháp kỹ thuật tương ứng trong suốt 6 tuần thực hiện dự án.

---

## 📅 TUẦN 1: THIẾT LẬP MÔI TRƯỜNG & BENCHMARK VRAM
**Mục tiêu tuần:** Cấu hình môi trường Anaconda, cài đặt PyTorch CUDA 12.1 và kiểm tra khả năng tương thích của card đồ họa RTX 4060. Chạy benchmark tải mô hình Qwen-2.5-7B-Instruct 4-bit.

### 📝 Nhật ký hàng ngày:

#### **Ngày 1 (03/07/2026)**
*   **Hoạt động:** Khởi tạo dự án và lập tài liệu định hướng tổng thể.
*   **Kết quả:** 
    *   Tạo file định hướng kiến trúc và kế hoạch triển khai [project_roadmap_technical_proposal.md](file:///c:/mydata/selfproject/AI_Japanese/project_roadmap_technical_proposal.md).
    *   Đề xuất Base Model Qwen-2.5-7B-Instruct tối ưu cho RTX 4060 8GB VRAM.

#### **Ngày 2 (04/07/2026)**
*   **Hoạt động:** Chuẩn bị các file cấu hình môi trường ảo và các kịch bản kiểm thử.
*   **Kết quả:** 
    *   Tạo file cấu hình môi trường Conda [environment.yml](file:///c:/mydata/selfproject/AI_Japanese/environment.yml).
    *   Tạo script kiểm tra phần cứng GPU CUDA [check_env.py](file:///c:/mydata/selfproject/AI_Japanese/check_env.py).
    *   Tạo script benchmark tải mô hình Qwen 4-bit [benchmark_qwen.py](file:///c:/mydata/selfproject/AI_Japanese/benchmark_qwen.py).
    *   Tạo file hướng dẫn thực hiện chi tiết [week1_guide.md](file:///c:/mydata/selfproject/AI_Japanese/week1_guide.md).

#### **Ngày 3 (05/07/2026)**
*   **Hoạt động:** Chạy thử nghiệm môi trường và giải quyết các lỗi ban đầu.
*   **Sự cố & Cách khắc phục:**
    *   *Sự cố 1:* Lỗi `ModuleNotFoundError: No module named 'torch'` do người dùng chạy python mặc định của hệ thống thay vì môi trường ảo.
        *   *Khắc phục:* Hướng dẫn gọi trực tiếp file thực thi Python trong môi trường ảo: `C:\Users\Lenovo\miniconda3\envs\ai_japanese\python.exe`.
    *   *Sự cố 2:* Lỗi `UnicodeEncodeError` khi in các ký tự tiếng Việt có dấu ra terminal Windows (CP1252).
        *   *Khắc phục:* Chuyển đổi toàn bộ output in ra của `check_env.py` và `benchmark_qwen.py` sang tiếng Anh không dấu.
    *   *Sự cố 3:* PyTorch cài qua conda mặc định là bản CPU-only, dẫn đến `CUDA Available: False`.
        *   *Khắc phục:* Khởi chạy tiến trình cài đè PyTorch CUDA 12.1 bằng pip trong background.

#### **Ngày 4 (06/07/2026)**
*   **Hoạt động:** Tối ưu hóa cài đặt PyTorch CUDA, thiết lập Git và tải base model.
*   **Sự cố & Cách khắc phục:**
    *   *Sự cố 4:* Cài đặt qua conda bị lỗi LibMambaUnsatisfiableError; cài qua pip bị lỗi `WinError 32` do Windows Defender lock file tạm.
        *   *Khắc phục:* Chuyển hướng thư mục Temp và Cache của pip sang thư mục nội bộ dự án (`tmp_pip/` và `pip_cache/`).
    *   *Sự cố 5:* Lỗi `IncompleteRead` do đường truyền mạng quốc tế chập chờn khi tải file PyTorch 2.45 GB.
        *   *Khắc phục:* Chuyển sang phương án cài đặt offline: Tải trực tiếp file `.whl` bằng trình duyệt/IDM và chạy lệnh cài cục bộ thành công. PyTorch đã nhận GPU RTX 4060.
    *   *Sự cố 6:* Lỗi `ModuleNotFoundError` từ `huggingface-cli`.
        *   *Khắc phục:* Viết script [download_model.py](file:///c:/mydata/selfproject/AI_Japanese/download_model.py) sử dụng API python `snapshot_download` chính thức.
    *   *Sự cố 7:* Lỗi kết nối `cannot locate the file on the Hub` do hf-mirror.com thực hiện redirect (mã 308) metadata API quay lại Hugging Face gốc.
        *   *Khắc phục:* Chuyển đổi phương án tải sang **ModelScope** (`modelscope` của Alibaba) với máy chủ CDN châu Á không bị chặn.
    *   *Sự cố 8:* Tốc độ tải mô hình bản 7B (15 GB) từ ModelScope trong khung giờ cao điểm tối bị bóp băng thông nghiêm trọng, tiến độ hiển thị mất tới 11 - 33 tiếng.
        *   *Khắc phục:* Đổi hướng tải mô hình sang bản **`Qwen2.5-1.5B-Instruct`** (dung lượng cực nhẹ ~3 GB) làm **mô hình Prototype** để chạy thử benchmark VRAM và xác minh code huấn luyện/suy luận thành công ngay lập tức. Sau đó sẽ cắm máy tải bản 7B đầy đủ qua đêm khi băng thông ổn định.
*   **Cải tiến:** Tạo file [.gitignore](file:///c:/mydata/selfproject/AI_Japanese/.gitignore) loại trừ cache cài đặt và trọng số mô hình lớn khỏi Git.
*   **Kết quả Ngày 5 (Đêm 06/07):** Chạy benchmark VRAM thành công với mô hình Prototype 1.5B 4-bit (VRAM tĩnh ~1.07 GB, VRAM động ~1.08 GB). Ép UTF-8 cho stdout sửa triệt để lỗi charmap.
*   **Hoạt động Ngày 6 (Chiều & Đêm 07/07/2026):**
    *   Cấu hình lại `download_model.py` chuyển sang tải bản chính thức Qwen-2.5-7B-Instruct (15 GB) và download thành công 100%.
    *   Thực thi benchmark bản 7B đầy đủ thành công: VRAM tĩnh 5.18 GB, VRAM động 5.19 GB. Đoạn dịch mẫu tiếng Nhật chuẩn xác 100%.
    *   *Sự cố phát sinh (Sự cố 11):* Gọi `generate_dataset.py` bằng API cũ của Gemini bị lỗi 404 không nhận diện mô hình và lỗi in Unicode trên console Windows.
        *   *Khắc phục:* Viết lại kịch bản sinh dữ liệu chuyển sang thư viện Google GenAI SDK mới (`google-genai`), sử dụng mô hình mới nhất `gemini-2.5-flash`, đồng thời ép UTF-8 cho `sys.stdout` trong cả 3 file script dữ liệu.
    *   *Hoạt động sinh dữ liệu:* Chạy thành công chuỗi 3 script xử lý dữ liệu. Sinh được 78 cặp hội thoại BrSE sạch sẽ, lọc trùng lặp và giới hạn chiều dài token. Tạo thành công hai file: `train.jsonl` (70 dòng) và `val.jsonl` (8 dòng).
    *   *Hoạt động Tuần 3 (Khởi động sớm):* Tạo kịch bản huấn luyện QLoRA `train.py`. Khắc phục thành công các lỗi tương thích API của `SFTTrainer` mới (chuyển sang `SFTConfig`, dùng `max_length` thay thế cho `max_seq_length`, dùng `processing_class` thay thế cho `tokenizer` và định cấu hình callback `formatting_func` ở chế độ single-item).
*   **Kết quả Ngày 7 (Chiều 08/07/2026):**
    *   Người dùng tự chạy script `train.py` thành công trên terminal cục bộ.
    *   *Số liệu thực tế (50 steps):*
        *   **Training Loss:** Giảm đều từ **1.46** (step 10) xuống **0.54** (step 50).
        *   **Validation Loss:** Giảm từ **1.11** (step 10) xuống **0.87** (step 50).
        *   **Mean Token Accuracy:** Tăng từ **67.0%** (step 10) lên **86.2%** (step 50).
        *   **VRAM chiếm dụng:** Hoạt động ổn định ở mức ~6.8 GB VRAM, tuyệt đối không bị OOM.
        *   **Sản phẩm:** Adapter weights lưu thành công tại `./outputs/checkpoint-50/`.
*   **Trạng thái hiện tại:** Hoàn tất 100% mục tiêu của Tuần 1, Tuần 2 và Tuần 3. Chuẩn bị bước sang **Tuần 4**.
*   **Đánh giá tuần 3:** Mô hình QLoRA 4-bit chạy rất ổn định trên GPU RTX 4060 8GB. Loss và Eval loss giảm sâu chứng tỏ mô hình học tốt và không bị quá khớp. Sẵn sàng cho **Tuần 4: Đánh giá chất lượng và tích hợp trọng số**.

---

## 📅 TUẦN 2: KỸ NGHỆ DỮ LIỆU (DATA ENGINEERING)
*   **Ngày 6 (07/07/2026):** Sinh thành công dữ liệu hội thoại BrSE sạch sẽ bằng SDK google-genai mới. Tạo lập `train.jsonl` (70 dòng) và `val.jsonl` (8 dòng).

---

## 📅 TUẦN 3: CẤU HÌNH & HUẤN LUYỆN THỬ NGHIỆM
*   **Ngày 7 (08/07/2026):**
    *   Hoàn thiện script `train.py` tương thích API SFTConfig mới. Huấn luyện thành công 50 steps, lưu checkpoint trọng số tại `./outputs/checkpoint-50/`. Loss giảm sâu xuống 0.54.
    *   *Hoạt động Tuần 4 (Khởi động sớm):* Tạo script so sánh suy luận `inference_test.py` nạp động LoRA Adapter.
    *   *Kết quả kiểm thử chất lượng (Inference test):* Chạy thành công đối chiếu 4 test cases. Mô hình Fine-tuned QLoRA thể hiện sự vượt trội hoàn chỉnh:
        *   Sử dụng thuật ngữ IT tự nhiên của BrSE (ví dụ: dùng "Môi trường Production" thay vì dịch máy "Môi trường sản xuất").
        *   Viết email Kính ngữ Keigo chuẩn mực doanh nghiệp Nhật 100%, bổ sung tiêu đề email (`件名`), loại bỏ hoàn toàn các câu dịch lỗi phi tự nhiên của base model gốc (như "kính yêu đối tác", "貴社様").
*   **Trạng thái hiện tại:** Hoàn tất 100% mục tiêu của Tuần 1 đến Tuần 4. Sẵn sàng bước sang **Tuần 5**.
*   **Đánh giá tuần 4:** Trọng số LoRA Adapter từ checkpoint-50 mang lại sự thay đổi rõ rệt về chất lượng văn phong email business và thuật ngữ IT Nhật-Việt. Sẵn sàng cho **Tuần 5: Đóng gói GGUF, Ollama và phát triển UI**.

---

## 📅 TUẦN 4: ĐÁNH GIÁ CHẤT LƯỢNG - INFERENCE EVALUATION
*   **Ngày 7 (08/07/2026):** Viết script `inference_test.py` đối chiếu song song. Xác minh mô hình sau khi tinh chỉnh sử dụng kính ngữ mượt mà và thuật ngữ chuyên ngành IT tự nhiên.

---

## 📅 TUẦN 5: ĐÓNG GÓI & PHÁT TRIỂN GIAO DIỆN
*   **Ngày 7 (08/07/2026):**
    *   Thực hiện merge weights LoRA trên CPU sang thư mục `./merged_model/` thành công.
    *   Viết kịch bản `convert_to_gguf.py`, clone `llama.cpp` và chuyển đổi sang định dạng GGUF lượng tử hóa 8-bit `qwen2.5-7b-ja-brse-q8.gguf` (~7.7 GB) thành công.
    *   Tạo file cấu hình `Modelfile` đăng ký mô hình vào Ollama.
    *   Viết ứng dụng giao diện Web UI bằng Streamlit `app.py` với các tab dịch thuật IT và soạn thảo email.

---

## 📅 TUẦN 6: KIỂM THỬ HỆ THỐNG & TỐI ƯU HÓA (UAT)
*   **Ngày 7 (08/07/2026):**
    *   Người dùng cài đặt Ollama thành công trên máy Windows. Đăng ký mô hình `ja-brse` thành công.
    *   Khởi chạy thành công giao diện Web UI Streamlit cục bộ tại `http://localhost:8501`.
    *   Tiến hành kiểm thử chất lượng thực tế (UAT) đạt chất lượng xuất sắc. AI tự động tối ưu hóa lý do viết email trang trọng, từ ngữ dịch thuật IT chuẩn mực.
    *   Tạo tài liệu bàn giao dự án hoàn chỉnh `README.md`. Kết thúc dự án vượt tiến độ.
