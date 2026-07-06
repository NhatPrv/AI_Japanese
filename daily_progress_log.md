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
*   **Hoạt động:** Tối ưu hóa cài đặt PyTorch CUDA và thiết lập Git.
*   **Sự cố & Cách khắc phục:**
    *   *Sự cố 4:* Cài đặt qua conda bị lỗi LibMambaUnsatisfiableError do thiếu các gói bổ trợ; cài qua pip bị lỗi `WinError 32` do Windows Defender lock file tạm trong thư mục Temp hệ thống.
        *   *Khắc phục:* Chuyển hướng thư mục Temp và Cache của pip sang thư mục nội bộ dự án (`tmp_pip/` và `pip_cache/`) để tránh bị Windows Defender quét tranh chấp.
    *   *Sự cố 5:* Lỗi `IncompleteRead` do đường truyền mạng quốc tế đến server PyTorch chập chờn khi tải file 2.45 GB.
        *   *Khắc phục:* Chuyển sang phương án **Cài đặt ngoại tuyến (Offline)**: Hướng dẫn người dùng tải trực tiếp file `.whl` bằng trình duyệt/IDM, sau đó cài offline bằng lệnh pip cục bộ.
*   **Cải tiến:** Tạo file [.gitignore](file:///c:/mydata/selfproject/AI_Japanese/.gitignore) để loại trừ môi trường ảo, cache cài đặt và trọng số mô hình lớn khỏi Git.
*   **Trạng thái hiện tại:** Người dùng đang thực hiện tải file `.whl` bằng trình duyệt để cài đặt offline PyTorch CUDA.

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
