import os
import sys
import io
import torch
import gc

# Ép terminal Windows (PowerShell/CMD) sử dụng bảng mã UTF-8 để in log tiếng Việt không bị lỗi charmap
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Kiểm tra các thư viện cần thiết trước khi huấn luyện
required_libs = ["peft", "trl", "accelerate", "datasets", "bitsandbytes"]
missing_libs = []
for lib in required_libs:
    try:
        __import__(lib)
    except ImportError:
        missing_libs.append(lib)

if missing_libs:
    print(f"Đang cài đặt các thư viện thiếu cho huấn luyện: {missing_libs}...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_libs)

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

def main():
    model_id = r"C:/Users/Lenovo/.cache/modelscope/qwen/Qwen2.5-7B-Instruct"
    train_file = "train.jsonl"
    val_file = "val.jsonl"
    output_dir = "./outputs"
    
    print("="*60)
    print("BẮT ĐẦU KHỞI TẠO TIẾN TRÌNH HUẤN LUYỆN QLORA (TUẦN 3)")
    print(f"Mô hình nền: {model_id}")
    print(f"Tập Train:  {train_file} | Tập Val: {val_file}")
    print("="*60)

    if not os.path.exists(train_file) or not os.path.exists(val_file):
        print("LỖI: Chưa có tập dữ liệu train.jsonl hoặc val.jsonl. Vui lòng chạy pipeline Tuần 2 trước.")
        sys.exit(1)

    # 1. Cấu hình BitsAndBytes để load mô hình 4-bit tiết kiệm VRAM
    print("\n[1/5] Đang cấu hình BitsAndBytes 4-bit...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    # 2. Tải Tokenizer và Mô hình nền
    print("\n[2/5] Đang nạp Tokenizer & Mô hình nền 4-bit...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right" # Rất quan trọng khi huấn luyện SFT để tránh lỗi lệch attention mask

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        local_files_only=True
    )

    # Chuẩn bị mô hình cho huấn luyện lượng tử (K-bit training)
    model = prepare_model_for_kbit_training(model)
    # Kích hoạt Gradient Checkpointing để tiết kiệm cực nhiều VRAM (~30-40%)
    model.gradient_checkpointing_enable()

    # 3. Cấu hình LoRA Adapter (Fine-tuning trọng số bổ sung)
    print("\n[3/5] Đang cấu hình LoRA Adapter...")
    peft_config = LoraConfig(
        r=16,                            # Độ rộng ma trận cập nhật bổ sung
        lora_alpha=32,                   # Tham số tỉ lệ scaling
        target_modules=[                 # Nhắm vào toàn bộ các lớp tuyến tính của Qwen-2.5 để học tối đa
            "q_proj", "k_proj", "v_proj", "o_proj", 
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # 4. Nạp dữ liệu huấn luyện
    print("\n[4/5] Đang nạp dữ liệu huấn luyện...")
    dataset = load_dataset("json", data_files={"train": train_file, "validation": val_file})

    def formatting_prompts_func(example):
        # example['messages'] là danh sách tin nhắn của 1 mẫu dữ liệu đơn lẻ (do SFTTrainer map với batched=False)
        return tokenizer.apply_chat_template(example['messages'], tokenize=False)

    # 5. Cấu hình Tham số Huấn luyện tối ưu bộ nhớ VRAM bằng SFTConfig của TRL mới
    print("\n[5/5] Thiết lập các tham số huấn luyện tối ưu VRAM...")
    training_args = SFTConfig(
        output_dir=output_dir,
        per_device_train_batch_size=1,        # Batch size tối thiểu
        gradient_accumulation_steps=4,         # Tích lũy gradient qua 4 bước (Effective Batch size = 4)
        learning_rate=2e-4,                    # Tốc độ học tối ưu cho LoRA
        logging_steps=10,                      # Ghi log sau mỗi 10 steps
        eval_strategy="steps",                 # Đánh giá val loss theo steps
        eval_steps=10,
        max_steps=50,                          # Chạy thử nghiệm 50 steps để kiểm tra độ ổn định bộ nhớ
        save_strategy="steps",
        save_steps=20,
        save_total_limit=2,                    # Giới hạn lưu tối đa 2 checkpoint tránh đầy bộ nhớ đĩa
        bf16=True,                             # Sử dụng bfloat16 cho GPU RTX 4060
        optim="paged_adamw_8bit",              # Optimizer 8-bit tiết kiệm VRAM tối đa
        gradient_checkpointing=True,           # Tái tính toán kích hoạt để chống tràn VRAM
        report_to="none",                      # Tắt kết nối log online
        fp16=False,
        max_length=512                         # max_length được cấu hình trực tiếp ở đây trong SFTConfig cho TRL mới
    )

    # Khởi tạo SFTTrainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        peft_config=peft_config,
        formatting_func=formatting_prompts_func,
        processing_class=tokenizer,            # Sử dụng processing_class thay cho tokenizer trong TRL mới
        args=training_args,
    )

    # Khởi chạy huấn luyện
    print("\n" + "="*60)
    print("MỌI THỨ ĐÃ SẴN SÀNG! KHỞI CHẠY HUẤN LUYỆN THỬ NGHIỆM...")
    print("="*60)
    
    # Dọn dẹp cache VRAM trước khi chạy
    gc.collect()
    torch.cuda.empty_cache()

    trainer.train()

    print("\n" + "="*60)
    print("HUẤN LUYỆN THỬ NGHIỆM HOÀN TẤT THÀNH CÔNG!")
    print(f"Mô hình adapter đã lưu tại: {output_dir}")
    print("="*60)

if __name__ == "__main__":
    main()
