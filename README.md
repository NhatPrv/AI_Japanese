# 🎓 AI Bridge Engineer (BrSE) Support Suite

AI Bridge Engineer Suite là một giải pháp AI cục bộ (Local AI) hoàn chỉnh được thiết kế và huấn luyện đặc biệt để hỗ trợ các Kỹ sư cầu nối (BrSE) dịch thuật thuật ngữ chuyên ngành IT Nhật-Việt và soạn thảo email doanh nghiệp bằng Kính ngữ Keigo chuẩn mực.

Dự án sử dụng mô hình nền **Qwen-2.5-7B-Instruct** và được tinh chỉnh bằng phương pháp **QLoRA 4-bit** tối ưu hóa trên cấu hình card đồ họa Laptop phổ thông (**RTX 4060 8GB VRAM**).

---

## 🚀 Tính năng nổi bật
1. **🌐 Trình dịch thuật IT chuyên sâu**: Chuyển ngữ chính xác các câu thoại chứa thuật ngữ IT kết hợp Nhật-Việt, tự động phát hiện và giải nghĩa các từ vựng kỹ thuật khó (như *本番環境*, *仕様書*, *デプロイ*...).
2. **✉️ Soạn thảo Email Kính ngữ (Keigo)**: Tự động soạn thảo email business theo nhiều ngữ cảnh làm việc (báo lỗi Production, xin lỗi chậm trễ, nhờ review tài liệu, đặt lịch họp...). Sử dụng Kính ngữ (Sonkeigo, Kenjougo) tự nhiên, trang trọng theo đúng quy tắc văn hóa doanh nghiệp Nhật Bản.
3. **💻 Hoạt động cục bộ 100%**: Đóng gói định dạng **GGUF Q8_0** chạy mượt mà thông qua **Ollama** trên máy cá nhân, bảo mật tuyệt đối dữ liệu dự án của doanh nghiệp.

---

## 📁 Cấu trúc thư mục Dự án
*   `train.jsonl` / `val.jsonl`: Tập dữ liệu huấn luyện (hội thoại BrSE sạch).
*   `generate_dataset.py` / `clean_dataset.py` / `split_dataset.py`: Pipeline sinh dữ liệu tự động từ Gemini API và tiền xử lý.
*   `train.py`: Script huấn luyện QLoRA 4-bit tối ưu hóa VRAM (~6.8 GB) bằng `SFTConfig`.
*   `inference_test.py`: Script chạy thử nghiệm và đối chiếu chất lượng mô hình trước/sau khi train.
*   `merge_weights.py`: Script gộp trọng số Adapter LoRA vào Base Model 7B (chạy trên CPU để chống OOM).
*   `convert_to_gguf.py`: Script tự động clone `llama.cpp` và lượng tử hóa mô hình đã gộp sang GGUF 8-bit (`q8_0`).
*   `Modelfile`: File cấu hình đăng ký mô hình vào Ollama.
*   `app.py`: Giao diện Web UI trực quan bằng Streamlit.
*   `daily_progress_log.md`: Nhật ký tiến độ thực thi dự án qua 6 tuần.

---

## 🛠️ Hướng dẫn cài đặt và vận hành nhanh

### 1. Yêu cầu hệ thống
*   **Hệ điều hành**: Windows 10/11.
*   **Card đồ họa**: NVIDIA GPU hỗ trợ CUDA (Khuyến nghị RTX 3060/4060 8GB VRAM trở lên).
*   **RAM**: 16 GB hệ thống trở lên.
*   **Phần mềm bổ trợ**: **Ollama for Windows** (đã cài đặt).

### 2. Thiết lập Môi trường ảo (Conda)
Mở PowerShell tại thư mục dự án và chạy các lệnh:
```powershell
# Tạo và kích hoạt môi trường ảo Python 3.10
conda env create -f environment.yml
conda activate ai_japanese

# Cài đặt thư viện Streamlit và các gói bổ trợ
pip install streamlit requests gguf
```

### 3. Đăng ký mô hình vào Ollama
Đảm bảo phần mềm Ollama đã được khởi chạy dưới khay hệ thống, sau đó thực hiện lệnh:
```powershell
# Di chuyển tới thư mục chứa Modelfile và đăng ký mô hình tên "ja-brse"
ollama create ja-brse -f Modelfile
```

### 4. Khởi chạy Giao diện Web (Cách nhanh nhất)
Từ các lần sau trở đi, bạn không cần mở PowerShell hay gõ lệnh gì nữa. Bạn chỉ cần vào thư mục dự án và **click đúp chuột** vào file:
👉 **`run_app.bat`** (File chạy nhanh tự động đã tạo sẵn cho bạn).

*Trình duyệt sẽ tự động bật lên và kết nối vào giao diện Web UI tại địa chỉ: `http://localhost:8501`.*

---

## 🎨 Trải nghiệm thực tế (Mẹo sử dụng)
*   **Tải trọng VRAM cực nhẹ**: Mô hình khi chạy qua Ollama chỉ chiếm khoảng **7.2 GB VRAM**, giúp máy tính hoạt động mát mẻ và bạn vẫn có thể làm việc song song các tác vụ khác.
*   **Kỹ năng BrSE thông minh**: Khi bạn nhập lý do lỗi bằng tiếng Việt một cách thô mộc (ví dụ: *"Quên sửa code kịp"*), mô hình sẽ tự động tối ưu hóa câu chữ sang tiếng Nhật chuyên nghiệp và trang trọng (ví dụ: *"バグの再現性が低く、詳細な調査に時間がかかったため"* - do tỉ lệ tái hiện bug thấp và cần thêm thời gian khảo sát kỹ lưỡng).

---
*Dự án được xây dựng và hoàn thiện bởi sự cộng tác giữa Bạn và Antigravity AI Assistant.*
