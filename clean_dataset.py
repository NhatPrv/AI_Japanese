import os
import sys
import io
import json

# Ép terminal Windows (PowerShell/CMD) sử dụng bảng mã UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from transformers import AutoTokenizer
except ImportError:
    print("Đang cài đặt thư viện 'transformers'...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
    from transformers import AutoTokenizer

def jaccard_similarity(str1, str2):
    # Tính toán độ tương đồng từ vựng đơn giản để lọc trùng lặp ngữ nghĩa
    words1 = set(str1.lower().split())
    words2 = set(str2.lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    if not union:
        return 0.0
    return len(intersection) / len(union)

def main():
    input_file = "raw_dataset.jsonl"
    output_file = "cleaned_dataset.jsonl"
    
    # Sử dụng cache local của mô hình 1.5B đã tải thành công để load Tokenizer offline
    model_path = r"C:/Users/Lenovo/.cache/modelscope/qwen/Qwen2.5-1.5B-Instruct"
    
    print("="*60)
    print("BẮT ĐẦU LÀM SẠCH VÀ TIỀN XỬ LÝ DỮ LIỆU")
    print(f"Đầu vào: {input_file} | Đầu ra: {output_file}")
    print("="*60)
    
    if not os.path.exists(input_file):
        print(f"LỖI: Không tìm thấy tệp dữ liệu thô '{input_file}'! Vui lòng chạy generate_dataset.py trước.")
        sys.exit(1)
        
    print("Đang tải Tokenizer để đếm số lượng token...")
    try:
        if os.path.exists(model_path):
            tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
            print("-> Đã tải Tokenizer cục bộ từ cache.")
        else:
            tokenizer = AutoTokenizer.from_pretrained("qwen/Qwen2.5-1.5B-Instruct")
            print("-> Đã tải Tokenizer online.")
    except Exception as e:
        print(f"Lỗi tải Tokenizer: {e}")
        sys.exit(1)
        
    cleaned_data = []
    user_sentences = []
    
    # Các thông số thống kê
    total_lines = 0
    invalid_format = 0
    too_long = 0
    duplicates = 0
    
    # Đọc dữ liệu
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            
            # 1. Kiểm tra định dạng JSON
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                invalid_format += 1
                continue
                
            # Kiểm tra cấu trúc hội thoại chuẩn
            if "messages" not in data or not isinstance(data["messages"], list):
                invalid_format += 1
                continue
                
            # Lấy nội dung câu hỏi của user để lọc trùng
            user_content = ""
            for msg in data["messages"]:
                if msg.get("role") == "user":
                    user_content = msg.get("content", "")
                    break
            
            # 2. Kiểm tra trùng lặp (Deduplication - Ngưỡng 80% trùng từ vựng)
            is_duplicate = False
            for prev_sentence in user_sentences:
                similarity = jaccard_similarity(user_content, prev_sentence)
                if similarity > 0.8:
                    is_duplicate = True
                    break
            
            if is_duplicate:
                duplicates += 1
                continue
                
            # 3. Kiểm tra độ dài Token tối đa (Giới hạn 512 tokens để tránh OOM)
            # Áp dụng format template chatML của Qwen để đếm chính xác số token đầu vào
            try:
                tokenized_prompt = tokenizer.apply_chat_template(
                    data["messages"], 
                    tokenize=True, 
                    add_generation_prompt=False
                )
                token_count = len(tokenized_prompt)
            except Exception:
                # Nếu apply template bị lỗi, đếm số từ thô sơ bộ
                token_count = sum(len(msg.get("content", "").split()) for msg in data["messages"])
                
            if token_count > 512:
                too_long += 1
                continue
                
            # Lưu dữ liệu đạt chuẩn
            cleaned_data.append(line)
            user_sentences.append(user_content)
            
    # Ghi dữ liệu sạch ra file
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in cleaned_data:
            f.write(line + '\n')
            
    print("\n" + "="*60)
    print("BÁO CÁO KẾT QUẢ LÀM SẠCH DỮ LIỆU:")
    print(f" - Tổng số dòng dữ liệu thô đầu vào: {total_lines}")
    print(f" - Loại bỏ dòng sai định dạng JSON:  {invalid_format}")
    print(f" - Loại bỏ dòng bị trùng lặp:        {duplicates}")
    print(f" - Loại bỏ dòng quá dài (>512 tokens): {too_long}")
    print(f" -> Tổng số dòng sạch đầu ra:        {len(cleaned_data)}")
    print(f"Tệp tin dữ liệu sạch đã lưu tại: {output_file}")
    print("="*60)

if __name__ == "__main__":
    main()
