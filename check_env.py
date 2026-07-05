import sys
import torch
import psutil

def check_environment():
    print("="*50)
    print("CHECKING HARDWARE ENVIRONMENT & LIBRARIES")
    print("="*50)
    
    # 1. Python version
    print(f"Python Version: {sys.version}")
    
    # 2. System RAM
    ram = psutil.virtual_memory()
    print(f"System RAM: Total {ram.total / (1024**3):.2f} GB | Available {ram.available / (1024**3):.2f} GB")
    
    # 3. PyTorch & CUDA
    print(f"PyTorch Version: {torch.__version__}")
    cuda_available = torch.cuda.is_available()
    print(f"CUDA Available in PyTorch: {cuda_available}")
    
    if cuda_available:
        print(f"CUDA Version in PyTorch: {torch.version.cuda}")
        gpu_count = torch.cuda.device_count()
        print(f"GPU Count: {gpu_count}")
        
        for i in range(gpu_count):
            properties = torch.cuda.get_device_properties(i)
            name = properties.name
            total_memory = properties.total_memory / (1024**3) # Convert bytes to GB
            major = properties.major
            minor = properties.minor
            
            print(f"\nGPU {i}: {name}")
            print(f"  - Total VRAM: {total_memory:.2f} GB")
            print(f"  - Compute Capability: {major}.{minor}")
            
            # Check RTX 4060
            if "4060" in name:
                print("  -> RTX 4060 detected. Configuration ready for QLoRA parameters.")
            
            allocated = torch.cuda.memory_allocated(i) / (1024**3)
            reserved = torch.cuda.memory_reserved(i) / (1024**3)
            print(f"  - Currently allocated memory (Allocated): {allocated:.4f} GB")
            print(f"  - Currently reserved memory (Reserved): {reserved:.4f} GB")
    else:
        print("\n[WARNING]: CUDA is not available! Please check your NVIDIA GPU drivers or PyTorch installation.")
    
    print("="*50)

if __name__ == "__main__":
    check_environment()
