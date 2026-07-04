# HƯỚNG DẪN THỰC THI TUẦN 1: THIẾT LẬP MÔI TRƯỜNG & BENCHMARK VRAM

Do môi trường hệ điều hành Windows mặc định không cấu hình lệnh `conda` trong PowerShell thông thường (để tránh xung đột), bạn vui lòng thực hiện các bước sau bằng công cụ dòng lệnh **Anaconda Prompt** hoặc **Miniconda Prompt** của bạn.

---

### BƯỚC 1: Khởi tạo Môi trường Conda
Mở **Anaconda Prompt** (hoặc Miniconda Prompt) và di chuyển vào thư mục dự án:
```cmd
cd c:\mydata\selfproject\AI_Japanese
```

Sau đó chạy lệnh tạo môi trường mới từ file `environment.yml` đã được cấu hình sẵn:
```cmd
conda env create -f environment.yml
```
*(Quá trình này sẽ tải Python 3.10, PyTorch tương thích CUDA 12.1 và các thư viện cần thiết. Có thể mất khoảng 5-10 phút tùy thuộc vào tốc độ mạng của bạn).*

---

### BƯỚC 2: Kích hoạt Môi trường & Xác minh GPU CUDA
Sau khi tạo xong môi trường, hãy kích hoạt nó:
```cmd
conda activate ai_japanese
```

Chạy script kiểm tra phần cứng để đảm bảo PyTorch nhận diện đúng card RTX 4060 8GB VRAM:
```cmd
python check_env.py
```
**Yêu cầu đầu ra:** Terminal phải in ra thông tin chi tiết về GPU `GeForce RTX 4060 Laptop GPU` cùng với dung lượng VRAM thực tế khả dụng (~8GB).

---

### BƯỚC 3: Chạy Benchmark Mô hình Qwen-2.5-7B-Instruct (4-bit)
Sau khi verify GPU hoạt động thành công, chạy script đo lường bộ nhớ VRAM tĩnh và động khi load mô hình:
```cmd
python benchmark_qwen.py
```
*(Mô hình `Qwen/Qwen2.5-7B-Instruct` ở dạng 4-bit nặng khoảng 4.5 GB. Script sẽ tự động tải các file mô hình từ Hugging Face về máy local của bạn và chạy một câu lệnh dịch thử để đo lượng VRAM đỉnh).*

---

### BƯỚC 4: Báo cáo kết quả
Sau khi chạy xong hai script trên, bạn hãy gửi lại kết quả in ra trên terminal (đặc biệt là lượng VRAM tiêu thụ ở các bước tĩnh/động trong `benchmark_qwen.py`) để tôi cập nhật báo cáo và chuẩn bị kế hoạch cho **Tuần 2**.
