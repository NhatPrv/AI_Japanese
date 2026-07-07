import os
import sys
import json
import random

def main():
    input_file = "cleaned_dataset.jsonl"
    train_file = "train.jsonl"
    val_file = "val.jsonl"
    
    # Thiết lập random seed cố định để việc chia tập dữ liệu có tính tái lập (reproducibility)
    random.seed(42)
    
    print("="*60)
    print("BẮT ĐẦU PHÂN CHIA TẬP DỮ LIỆU TRAIN / VAL")
    print(f"Đầu vào: {input_file}")
    print("="*60)
    
    if not os.path.exists(input_file):
        print(f"LỖI: Không tìm thấy tệp dữ liệu sạch '{input_file}'! Vui lòng chạy clean_dataset.py trước.")
        sys.exit(1)
        
    # Đọc toàn bộ các dòng dữ liệu sạch
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    total_samples = len(lines)
    if total_samples < 10:
        print("LỖI: Số lượng dòng dữ liệu sạch quá ít để thực hiện phân chia (cần tối thiểu 10 dòng).")
        sys.exit(1)
        
    # Trộn ngẫu nhiên dữ liệu (Shuffle)
    random.shuffle(lines)
    
    # Tính toán mốc phân chia (90% Train, 10% Val)
    split_index = int(total_samples * 0.9)
    
    train_lines = lines[:split_index]
    val_lines = lines[split_index:]
    
    # Ghi tập Train
    with open(train_file, 'w', encoding='utf-8') as f:
        for line in train_lines:
            f.write(line + '\n')
            
    # Ghi tập Val
    with open(val_file, 'w', encoding='utf-8') as f:
        for line in val_lines:
            f.write(line + '\n')
            
    print("\n" + "="*60)
    print("BÁO CÁO PHÂN CHIA DỮ LIỆU:")
    print(f" - Tổng số dòng dữ liệu sạch:  {total_samples}")
    print(f" - Tập huấn luyện (Train - 90%): {len(train_lines)} dòng -> Lưu tại: {train_file}")
    print(f" - Tập đánh giá (Val - 10%):    {len(val_lines)} dòng -> Lưu tại: {val_file}")
    print("="*60)

if __name__ == "__main__":
    main()
