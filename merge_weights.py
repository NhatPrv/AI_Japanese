import os
import sys
import io
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Ép terminal Windows sử dụng bảng mã UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    base_model_path = r"C:/Users/Lenovo/.cache/modelscope/qwen/Qwen2.5-7B-Instruct"
    adapter_path = "./outputs/checkpoint-50"
    output_path = "./merged_model"
    
    print("="*60)
    print("BẮT ĐẦU GỘP TRỌNG SỐ LORA VÀO BASE MODEL (FP16)")
    print(f"Base Model: {base_model_path}")
    print(f"Adapter LoRA: {adapter_path}")
    print(f"Đầu ra Merged: {output_path}")
    print("="*60)

    if not os.path.exists(adapter_path):
        print(f"LỖI: Không tìm thấy thư mục LoRA Adapter tại '{adapter_path}'!")
        sys.exit(1)

    print("\n[1/3] Đang nạp Tokenizer & Base Model trên CPU (tránh tràn VRAM)...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, local_files_only=True)
    
    # Load base model ở dạng FP16 hoàn toàn trên CPU để tận dụng RAM 16GB hệ thống, tránh tràn 8GB VRAM
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16,
        device_map={"": "cpu"}, # Ép buộc nạp trên CPU
        local_files_only=True
    )

    print("\n[2/3] Đang nạp LoRA Adapter và thực hiện gộp trọng số (Merge)...")
    # Load adapter
    model = PeftModel.from_pretrained(base_model, adapter_path)
    # Gộp LoRA weights vào base weights và unload adapter layers
    merged_model = model.merge_and_unload()

    print("\n[3/3] Đang lưu mô hình đã gộp vào thư mục merged_model...")
    merged_model.save_pretrained(output_path, max_shard_size="5GB")
    tokenizer.save_pretrained(output_path)

    print("\n" + "="*60)
    print("GỘP TRỌNG SỐ THÀNH CÔNG!")
    print(f"Mô hình hoàn chỉnh đã lưu tại: {output_path}")
    print("="*60)

if __name__ == "__main__":
    main()
