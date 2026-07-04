import torch
import gc
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

def print_vram_status(step_name):
    if torch.cuda.is_available():
        # Thu dọn rác và giải phóng cache CUDA trước khi đo
        gc.collect()
        torch.cuda.empty_cache()
        allocated = torch.cuda.memory_allocated(0) / (1024**3)
        reserved = torch.cuda.memory_reserved(0) / (1024**3)
        print(f"[{step_name}] VRAM Đã Dùng (Allocated): {allocated:.4f} GB | VRAM Được Cấp Phát (Reserved): {reserved:.4f} GB")
    else:
        print(f"[{step_name}] CUDA chưa khả dụng.")

def run_benchmark():
    model_id = "Qwen/Qwen2.5-7B-Instruct"
    print("="*60)
    print(f"BENCHMARK VRAM BASELINE VỚI MÔ HÌNH: {model_id}")
    print("="*60)

    print_vram_status("1. TRẠNG THÁI BAN ĐẦU")

    # 1. Cấu hình load 4-bit thông qua BitsAndBytes
    print("\nKhởi tạo cấu hình 4-bit BitsAndBytesConfig...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,       # Double quantization giúp tiết kiệm thêm ~0.4 bit trên mỗi tham số
        bnb_4bit_quant_type="nf4",            # NF4 tối ưu hóa phân phối trọng số của LLM
        bnb_4bit_compute_dtype=torch.bfloat16 # Dùng bfloat16 cho các lớp trung gian (RTX 4060 Laptop hỗ trợ native)
    )

    # 2. Tải Tokenizer
    print("\nĐang tải Tokenizer từ Hugging Face...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        print("Tải Tokenizer thành công.")
    except Exception as e:
        print(f"Lỗi tải Tokenizer: {e}")
        return

    # 3. Tải Mô hình gốc đã quantize 4-bit
    print(f"\nĐang tải Base Model '{model_id}' ở dạng 4-bit...")
    print("Lưu ý: Quá trình này sẽ tải khoảng ~4.5GB file shard của mô hình nếu chạy lần đầu.")
    start_time = time.time()
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",                # Tự động mapping các layer vào GPU khả dụng
            torch_dtype=torch.bfloat16
        )
        load_time = time.time() - start_time
        print(f"-> Tải mô hình thành công sau {load_time:.2f} giây.")
        print_vram_status("2. TRẠNG THÁI SAU KHI TẢI MÔ HÌNH (VRAM Tĩnh)")
        
        # 4. Thử nghiệm suy luận để đánh giá VRAM động (Dynamic Peak Memory)
        print("\nChạy thử nghiệm suy luận (Inference test)...")
        prompt = "Dịch câu sau sang tiếng Nhật: 'Chào buổi sáng, tôi là kỹ sư cầu nối phụ trách dự án này.'"
        messages = [
            {"role": "system", "content": "Bạn là một trợ lý dịch thuật IT Nhật-Việt hữu ích."},
            {"role": "user", "content": prompt}
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([text], return_tensors="pt").to("cuda")
        
        start_gen = time.time()
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=128,
                temperature=0.3,
                do_sample=True
            )
        gen_time = time.time() - start_gen
        
        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        print(f"\n[Kết quả từ AI]:\n{response.strip()}")
        print(f"\n-> Thời gian sinh từ: {gen_time:.2f} giây.")
        
        print_vram_status("3. TRẠNG THÁI SAU SUY LUẬN (VRAM Động)")
        
    except Exception as e:
        print(f"\n[LỖI]: Không thể tải hoặc chạy benchmark mô hình. Chi tiết: {e}")
        print("\nGợi ý khắc phục:")
        print("1. Hãy đảm bảo bạn đã cài đặt thư viện 'bitsandbytes' và 'accelerate'.")
        print("2. Đảm bảo driver đồ họa NVIDIA của bạn đã được cập nhật phiên bản mới nhất.")
        print("3. Kiểm tra kết nối mạng kết nối tới Hugging Face (hoặc chạy 'huggingface-cli login' nếu cần token xác thực).")
    
    print("="*60)

if __name__ == "__main__":
    run_benchmark()
