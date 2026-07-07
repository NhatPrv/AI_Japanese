import sys
import io

# Ép terminal Windows (PowerShell/CMD) sử dụng bảng mã UTF-8 để in ký tự tiếng Nhật và tiếng Việt có dấu không bị lỗi charmap
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import torch
import gc
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

def print_vram_status(step_name):
    if torch.cuda.is_available():
        # Clean memory and empty cache
        gc.collect()
        torch.cuda.empty_cache()
        allocated = torch.cuda.memory_allocated(0) / (1024**3)
        reserved = torch.cuda.memory_reserved(0) / (1024**3)
        print(f"[{step_name}] VRAM Allocated: {allocated:.4f} GB | VRAM Reserved: {reserved:.4f} GB")
    else:
        print(f"[{step_name}] CUDA is not available.")

def run_benchmark():
    # Sẽ tự động trỏ tới thư mục cục bộ của ModelScope từ script download_model.py
    model_id = r"C:/Users/Lenovo/.cache/modelscope/qwen/Qwen2.5-7B-Instruct"
    print("="*60)
    print(f"VRAM BENCHMARK FOR MODEL: {model_id}")
    print("="*60)

    print_vram_status("1. INITIAL STATE")

    # 1. Setup 4-bit config via BitsAndBytes
    print("\nInitializing BitsAndBytesConfig for 4-bit...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,       # Saves an additional ~0.4 bits/parameter
        bnb_4bit_quant_type="nf4",            # NF4 is optimized for normal-distributed LLM weights
        bnb_4bit_compute_dtype=torch.bfloat16 # Using bfloat16 for computation
    )

    # 2. Load Tokenizer
    print("\nLoading Tokenizer...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        print("Tokenizer loaded successfully.")
    except Exception as e:
        print(f"Failed to load Tokenizer: {e}")
        return

    # 3. Load Base Model in 4-bit
    print(f"\nLoading Base Model in 4-bit...")
    start_time = time.time()
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map="auto",                # Automatically map layers to GPU
            torch_dtype=torch.bfloat16
        )
        load_time = time.time() - start_time
        print(f"-> Model loaded successfully in {load_time:.2f} seconds.")
        print_vram_status("2. STATE AFTER LOADING MODEL (Static VRAM)")
        
        # 4. Run sample inference to measure dynamic VRAM (Peak Memory)
        print("\nRunning a sample inference test...")
        prompt = "Dịch câu sau sang tiếng Nhật: Chào buổi sáng, tôi là kỹ sư phụ trách dự án này."
        messages = [
            {"role": "system", "content": "You are a helpful IT translator."},
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
        print(f"\n[AI Response]:\n{response.strip()}")
        print(f"\n-> Generation time: {gen_time:.2f} seconds.")
        
        print_vram_status("3. STATE AFTER INFERENCE (Dynamic VRAM)")
        
    except Exception as e:
        print(f"\n[ERROR]: Failed to load or run model benchmark. Details: {e}")
        print("\nSuggestions:")
        print("1. Check if 'bitsandbytes' and 'accelerate' libraries are installed.")
        print("2. Ensure NVIDIA graphics driver is updated.")
        print("3. Check internet connection.")
    
    print("="*60)

if __name__ == "__main__":
    run_benchmark()
