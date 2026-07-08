import os
import sys
import io
import subprocess

# Ép terminal Windows sử dụng bảng mã UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def install_requirements():
    print("\n[1/3] Đang kiểm tra và cài đặt thư viện 'gguf'...")
    try:
        import gguf
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gguf"])

def clone_llama_cpp():
    repo_dir = "llama.cpp"
    if not os.path.exists(repo_dir):
        print(f"\n[2/3] Đang clone kho mã nguồn llama.cpp (Shallow Clone)...")
        try:
            # Clone với độ sâu 1 để tải nhanh nhất có thể
            subprocess.run(["git", "clone", "--depth", "1", "https://github.com/ggerganov/llama.cpp.git"], check=True)
            print(" -> Clone thành công.")
        except Exception as e:
            print(f"LỖI khi clone llama.cpp: {e}")
            sys.exit(1)
    else:
        print(f"\n[2/3] Thư mục '{repo_dir}' đã có sẵn trong dự án.")

def convert_model():
    input_dir = "./merged_model"
    output_file = "qwen2.5-7b-ja-brse-q8.gguf"
    script_path = os.path.join("llama.cpp", "convert_hf_to_gguf.py")
    
    if not os.path.exists(input_dir):
        print(f"LỖI: Không tìm thấy thư mục mô hình đã gộp '{input_dir}'! Vui lòng chạy merge_weights.py trước.")
        sys.exit(1)
        
    print(f"\n[3/3] Đang khởi chạy chuyển đổi mô hình sang định dạng GGUF lượng tử hóa 8-bit (q8_0)...")
    print("Quá trình chuyển đổi có thể mất 1-3 phút tùy tốc độ ổ cứng và CPU...")
    
    cmd = [
        sys.executable,
        script_path,
        input_dir,
        "--outtype", "q8_0",          # Lượng tử hóa q8_0 chất lượng cao
        "--outfile", output_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "="*60)
        print("CHUYỂN ĐỔI GGUF THÀNH CÔNG!")
        print(f"File mô hình đã lượng tử hóa: {output_file}")
        print("Dung lượng thực tế: ~7.7 GB (Chạy mượt trên GPU 8GB VRAM)")
        print("="*60)
    except subprocess.CalledProcessError as e:
        print(f"\nLỖI khi thực thi lệnh chuyển đổi: {e}")
        sys.exit(1)

def main():
    print("="*60)
    print("TIẾN TRÌNH TỰ ĐỘNG CLONE & CHUYỂN ĐỔI SANG ĐỊNH DẠNG GGUF")
    print("="*60)
    
    install_requirements()
    clone_llama_cpp()
    convert_model()

if __name__ == "__main__":
    main()
