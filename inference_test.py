import os
import sys
import io
import torch
import gc
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# Ép terminal Windows (PowerShell/CMD) sử dụng bảng mã UTF-8 để in ký tự tiếng Nhật/tiếng Việt không bị lỗi charmap
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Các câu test đánh giá định tính chất lượng mô hình
test_cases = [
    {
        "type": "IT Term Translation",
        "prompt": "Dịch câu sau sang tiếng Nhật: Vui lòng xác nhận tài liệu đặc tả thiết kế (仕様書) và môi trường phát triển (開発環境) trước khi tiến hành triển khai (デプロイ)."
    },
    {
        "type": "IT Term Explain",
        "prompt": "Giải thích ý nghĩa của thuật ngữ '本番環境' trong dự án phần mềm và dịch sang tiếng Việt."
    },
    {
        "type": "Email Keigo (Sonkeigo/Teineigo)",
        "prompt": "Viết email ngắn bằng kính ngữ Keigo trang trọng gửi khách hàng Nhật để báo cáo tiến độ dự án bị chậm trễ và xin lỗi đối tác."
    },
    {
        "type": "Email Keigo (Review request)",
        "prompt": "Viết email bằng kính ngữ Keigo gửi đối tác Nhật để nhờ họ review tài liệu thiết kế chi tiết (仕様書) và phản hồi ý kiến."
    }
]

def generate_response(model, tokenizer, prompt, title):
    messages = [
        {"role": "system", "content": "Bạn là một Kỹ sư cầu nối AI (AI Bridge Engineer) chuyên nghiệp, hỗ trợ dịch thuật IT Nhật-Việt và chuẩn hóa email Kính ngữ Keigo."},
        {"role": "user", "content": prompt}
    ]
    
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.3,
            do_sample=True,
            top_p=0.9
        )
    
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return response.strip()

def main():
    base_model_id = r"C:/Users/Lenovo/.cache/modelscope/qwen/Qwen2.5-7B-Instruct"
    adapter_dir = "./outputs/checkpoint-50"
    
    print("="*60)
    print("BẮT ĐẦU CHẠY THỬ NGHIỆM ĐÁNH GIÁ CHẤT LƯỢNG MÔ HÌNH (TUẦN 4)")
    print(f"Base Model: {base_model_id}")
    print(f"Lora Adapter: {adapter_dir}")
    print("="*60)

    if not os.path.exists(adapter_dir):
        print(f"LỖI: Không tìm thấy thư mục LoRA Adapter tại '{adapter_dir}'!")
        sys.exit(1)

    # 1. Cấu hình BitsAndBytes 4-bit
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    # 2. Tải Tokenizer và Base Model 4-bit
    print("\n[1/3] Đang nạp Base Model 4-bit...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, local_files_only=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        local_files_only=True
    )

    # 3. Thực hiện suy luận với Base Model gốc
    print("\n[2/3] Chạy suy luận thử nghiệm trên BASE MODEL GỐC...")
    base_responses = []
    for i, case in enumerate(test_cases):
        print(f" -> Đang chạy câu test {i+1}/{len(test_cases)}: {case['type']}...")
        res = generate_response(base_model, tokenizer, case['prompt'], "Base Model")
        base_responses.append(res)
        
    # Giải phóng cache VRAM
    gc.collect()
    torch.cuda.empty_cache()

    # 4. Gộp Adapter LoRA đã huấn luyện vào mô hình nền
    print("\n[3/3] Đang nạp trọng số LoRA Adapter đã huấn luyện...")
    # Load model peft động trên base model
    peft_model = PeftModel.from_pretrained(base_model, adapter_dir)
    
    print("\nChạy suy luận thử nghiệm trên MÔ HÌNH ĐÃ FINE-TUNED (QLoRA)...")
    ft_responses = []
    for i, case in enumerate(test_cases):
        print(f" -> Đang chạy câu test {i+1}/{len(test_cases)}: {case['type']}...")
        res = generate_response(peft_model, tokenizer, case['prompt'], "Fine-Tuned Model")
        ft_responses.append(res)

    # 5. In kết quả đối chiếu song song
    print("\n" + "="*80)
    print("BẢNG ĐỐI CHIẾU SO SÁNH CHẤT LƯỢNG SUY LUẬN")
    print("="*80)
    
    for i, case in enumerate(test_cases):
        print(f"\n📍 TEST CASE {i+1}: {case['type']}")
        print(f"📝 Yêu cầu (Prompt): {case['prompt']}")
        print("-" * 50)
        print(f"🤖 [BASE MODEL GỐC]:\n{base_responses[i]}")
        print("-" * 50)
        print(f"🎯 [MÔ HÌNH FINE-TUNED (QLoRA)]:\n{ft_responses[i]}")
        print("="*80)

if __name__ == "__main__":
    main()
