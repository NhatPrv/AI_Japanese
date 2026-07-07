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
*   **Hoạt động Ngày 6 (Chiều 07/07/2026):**
    *   Cấu hình lại `download_model.py` chuyển sang tải bản chính thức Qwen-2.5-7B-Instruct (15 GB).
    *   Khởi chạy tải trên local PowerShell.
    *   *Sự cố & Khắc phục (Sự cố 10):* Quá trình tải file lớn thỉnh thoảng gặp lỗi `Hash validation failed` hoặc `Connection broken (IncompleteRead)` do đường truyền mạng chập chập chờn.
        *   *Kết quả:* Trình quản lý ModelScope hoạt động cực kỳ tin cậy, tự động tính toán lại, kích hoạt cơ chế tự tải lại (retry 1/3) và tải nối tiếp (resume) chuẩn xác từ điểm bị ngắt.
    *   *Kết quả benchmark bản 7B chính thức:* Load thành công trong **21.73 giây**. Đo lường bộ nhớ thực tế:
        *   *VRAM Tĩnh (sau khi load 4-bit):* **5.1780 GB** (Allocated) | **5.3320 GB** (Reserved).
        *   *VRAM Động (suy luận sinh từ):* **5.1859 GB** (Allocated) | **5.3320 GB** (Reserved).
        *   *AI Response Test:* Câu dịch tiếng Nhật `"朝の挨拶です、私はこのプロジェクトを担当するエンジニアです。"` chuẩn ngữ pháp 100%.
*   **Trạng thái hiện tại:** Tải và benchmark thành công 100% mô hình chính thức Qwen-2.5-7B-Instruct. Hoàn tất toàn bộ mục tiêu của Tuần 1. Sẵn sàng bước sang **Tuần 2**.
*   **Đánh giá tuần 1:** Đã hoàn thành 100% mục tiêu thiết lập môi trường và benchmark VRAM baseline trên GPU RTX 4060. Sẵn sàng bước sang **Tuần 2: Kỹ nghệ Dữ liệu (Data Engineering)**.

---

## 📅 TUẦN 2: KỸ NGHỆ DỮ LIỆU (DATA ENGINEERING)
*(Sẽ cập nhật chi tiết hoạt động hàng ngày khi bước sang Tuần 2)*

---

## 📅 TUẦN 3: CẤU HÌNH & HUẤN LUYỆN THỬ NGHIỆM
*(Sẽ cập nhật chi tiết hoạt động hàng ngày khi bước sang Tuần 3)*

---

## 📅 TUẦN 4: HUẤN LUYỆN CHÍNH THỨC
*(Sẽ cập nhật chi tiết hoạt động hàng ngày khi bước sang Tuần 4)*

---

## 📅 TUẦN 5: ĐÓNG GÓI & PHÁT TRIỂN GIAO DIỆN
*(Sẽ cập nhật chi tiết hoạt động hàng ngày khi bước sang Tuần 5)*

---

## 📅 TUẦN 6: KIỂM THỬ HỆ THỐNG & TỐI ƯU HÓA
*(Sẽ cập nhật chi tiết hoạt động hàng ngày khi bước sang Tuần 6)*
