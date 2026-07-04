import sys
import torch
import psutil

def check_environment():
    print("="*50)
    print("KIỂM TRA MÔI TRƯỜNG PHẦN CỨNG & THƯ VIỆN")
    print("="*50)
    
    # 1. Kiểm tra Python version
    print(f"Phiên bản Python: {sys.version}")
    
    # 2. Kiểm tra System RAM
    ram = psutil.virtual_memory()
    print(f"RAM hệ thống: Tổng số {ram.total / (1024**3):.2f} GB | Khả dụng {ram.available / (1024**3):.2f} GB")
    
    # 3. Kiểm tra PyTorch và CUDA
    print(f"Phiên bản PyTorch: {torch.__version__}")
    cuda_available = torch.cuda.is_available()
    print(f"CUDA khả dụng với PyTorch: {cuda_available}")
    
    if cuda_available:
        print(f"Phiên bản CUDA trong PyTorch: {torch.version.cuda}")
        gpu_count = torch.cuda.device_count()
        print(f"Số lượng GPU được nhận diện: {gpu_count}")
        
        for i in range(gpu_count):
            properties = torch.cuda.get_device_properties(i)
            name = properties.name
            total_memory = properties.total_memory / (1024**3) # Convert bytes to GB
            major = properties.major
            minor = properties.minor
            
            print(f"\nGPU {i}: {name}")
            print(f"  - Tổng dung lượng VRAM: {total_memory:.2f} GB")
            print(f"  - Compute Capability: {major}.{minor}")
            
            # Kiểm tra xem có nhận diện đúng RTX 4060 không
            if "4060" in name:
                print("  -> Nhận diện đúng card RTX 4060. Sẵn sàng cấu hình các tham số QLoRA.")
            
            # Đo lường bộ nhớ đang sử dụng thực tế
            allocated = torch.cuda.memory_allocated(i) / (1024**3)
            reserved = torch.cuda.memory_reserved(i) / (1024**3)
            print(f"  - VRAM hiện tại đang dùng bởi PyTorch (Allocated): {allocated:.4f} GB")
            print(f"  - VRAM hiện tại đang cấp phát (Reserved): {reserved:.4f} GB")
    else:
        print("\n[CẢNH BÁO]: CUDA chưa khả dụng! Hãy cài đặt driver NVIDIA GPU phù hợp và bộ thư viện PyTorch CUDA.")
    
    print("="*50)

if __name__ == "__main__":
    check_environment()
