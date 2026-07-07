import os
import sys

try:
    from modelscope import snapshot_download
except ImportError:
    print("LỖI: Chưa cài đặt thư viện 'modelscope'.")
    sys.exit(1)

def main():
    # Tải bản 7B đầy đủ (15GB) để chạy huấn luyện và sử dụng thực tế.
    model_id = "qwen/Qwen2.5-7B-Instruct"
    
    print("="*60)
    print(f"BẮT ĐẦU TẢI MÔ HÌNH: {model_id}")
    print("Sử dụng máy chủ: Alibaba Cloud (ModelScope) - Dung lượng bản 7B đầy đủ ~15 GB")
    print("="*60)
    
    try:
        # Tải mô hình từ ModelScope
        model_dir = snapshot_download(model_id)
        
        print("\n" + "="*60)
        print("TẢI MÔ HÌNH THÀNH CÔNG!")
        print(f"Đường dẫn mô hình cục bộ: {model_dir}")
        print("="*60)
        
        # Cập nhật đường dẫn mô hình cục bộ vào file script benchmark_qwen.py
        update_benchmark_script(model_dir, model_id)
        
    except Exception as e:
        print(f"\nGặp lỗi trong quá trình tải mô hình: {e}")

def update_benchmark_script(model_dir, model_id):
    benchmark_file = "benchmark_qwen.py"
    if os.path.exists(benchmark_file):
        try:
            with open(benchmark_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chuẩn hóa đường dẫn Windows
            local_path = model_dir.replace('\\', '/')
            
            # Cập nhật đường dẫn cục bộ vào script benchmark
            # Vì benchmark_qwen.py ban đầu cấu hình model_id = "Qwen/Qwen2.5-7B-Instruct", chúng ta sẽ thay thế dòng này
            import re
            # Regex tìm dòng model_id = "..." hoặc model_id = r"..."
            pattern = r'model_id\s*=\s*(?:r?".*?"|".*?")'
            replacement = f'model_id = r"{local_path}"'
            
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)
                # Cập nhật thêm tên mô hình trong tiêu đề log in ra nếu cần
                content = content.replace("Qwen/Qwen2.5-7B-Instruct", model_id)
                
                with open(benchmark_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"-> Đã tự động cấu hình benchmark_qwen.py trỏ tới bản local 1.5B: {local_path}")
                print("Bây giờ bạn chỉ cần chạy: python benchmark_qwen.py")
            else:
                print("Không tìm thấy dòng cấu hình mặc định trong benchmark_qwen.py để tự động cập nhật.")
        except Exception as e:
            print(f"Lỗi cập nhật benchmark_qwen.py: {e}")
    else:
        print("Không tìm thấy file benchmark_qwen.py trong dự án để tự động cấu hình.")

if __name__ == "__main__":
    main()
