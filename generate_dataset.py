import os
import sys
import io
import json
import time

# Ép terminal Windows (PowerShell/CMD) sử dụng bảng mã UTF-8 để in ký tự tiếng Việt/tiếng Nhật không bị lỗi charmap
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Thử import thư viện Google GenAI mới
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Đang cài đặt thư viện mới 'google-genai'...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai"])
    from google import genai
    from google.genai import types

# 1. Tự động nạp API Key từ file .env nếu tồn tại
env_path = ".env"
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                if key.strip() == "GEMINI_API_KEY":
                    os.environ["GEMINI_API_KEY"] = val.strip()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("="*60)
    print("CẢNH BÁO: Chưa tìm thấy biến môi trường GEMINI_API_KEY!")
    print("Vui lòng thiết lập biến môi trường hoặc cấu hình trong file .env")
    print("="*60)
    sys.exit(1)

# Khởi tạo client GenAI mới (tự động nhận diện GEMINI_API_KEY từ os.environ)
client = genai.Client()

# 2. Định nghĩa bộ khung thuật ngữ IT Nhật - Việt
it_terms = [
    {"ja": "仕様書 (しようしょ)", "vi": "Tài liệu đặc tả thiết kế"},
    {"ja": "要件定義 (ようけんていぎ)", "vi": "Định nghĩa yêu cầu"},
    {"ja": "本番環境 (ほんばんかんきょう)", "vi": "Môi trường chạy thực tế (Production)"},
    {"ja": "開発環境 (かいはつかんきょう)", "vi": "Môi trường phát triển (Development)"},
    {"ja": "デプロイ", "vi": "Triển khai (Deploy)"},
    {"ja": "不具合 (ふぐあい) / バグ", "vi": "Lỗi phần mềm / Bug"},
    {"ja": "進捗 (しんちょく)", "vi": "Tiến độ"},
    {"ja": "納品 (のうひん)", "vi": "Bàn giao sản phẩm"},
    {"ja": "データベース (DB)", "vi": "Cơ sở dữ liệu"},
    {"ja": "検証 (けんしょう) / テスト", "vi": "Kiểm thử / Verify"}
]

# 3. Định nghĩa các tình huống giao tiếp Email BrSE (Keigo)
communication_scenarios = [
    "Báo cáo tiến độ dự án bị chậm trễ và xin lỗi đối tác Nhật",
    "Gửi tài liệu thiết kế chi tiết (Detail Design) yêu cầu đối tác review và feedback",
    "Giải trình nguyên nhân xảy ra lỗi nghiêm trọng (bug) trên môi trường Production và phương án khắc phục",
    "Gửi email xin lỗi vì phản hồi muộn và cung cấp thông tin giải đáp thắc mắc",
    "Đề xuất lịch họp khẩn cấp để làm rõ yêu cầu thay đổi (Change Request) của khách hàng",
    "Xác nhận đã nhận bàn giao (Delivery) và đang kiểm tra chất lượng",
    "Thông báo đã hoàn thành việc deploy lên môi trường Staging và nhờ đối tác test verify"
]

# System prompt hướng dẫn AI sinh dữ liệu chuẩn định dạng Conversational JSONL
SYSTEM_PROMPT = """
Bạn là một Chuyên gia Kỹ nghệ dữ liệu AI (AI Data Engineer). Nhiệm vụ của bạn là sinh dữ liệu chất lượng cao để huấn luyện một mô hình ngôn ngữ lớn (LLM) đóng vai trò là "Kỹ sư cầu nối ảo (AI Bridge Engineer)" chuyên dịch thuật thuật ngữ IT và viết email Kính ngữ (Keigo) Nhật - Việt.

Yêu cầu dữ liệu sinh ra phải:
1. Đạt độ chính xác 100% về thuật ngữ chuyên ngành IT giữa hai ngôn ngữ.
2. Đoạn văn tiếng Nhật email Keigo phải cực kỳ tự nhiên, trang trọng, sử dụng đúng ngữ pháp kính ngữ doanh nghiệp Nhật Bản (Sonkeigo, Kenjougo, Teineigo).
3. Mỗi cặp câu phải được đóng gói chính xác dưới định dạng Conversational JSONL của Hugging Face:
{"messages": [{"role": "system", "content": "Bạn là một Kỹ sư cầu nối AI (AI Bridge Engineer)..."}, {"role": "user", "content": "Câu hỏi của người dùng..."}, {"role": "assistant", "content": "Câu trả lời chuẩn của BrSE..."}]}

Hãy sinh dữ liệu thô dạng văn bản JSONL thuần túy, KHÔNG đặt trong block code markdown (không có ```json hay ``` ở đầu/cuối), mỗi dòng là một object JSON hoàn chỉnh.
"""

def generate_batch(prompt_desc, output_file):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_desc,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )
        lines = response.text.strip().split('\n')
        
        valid_count = 0
        with open(output_file, 'a', encoding='utf-8') as f:
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Loại bỏ markdown block nếu AI tự chèn vào
                if line.startswith("```"):
                    continue
                try:
                    # Verify xem line có phải JSON hợp lệ không
                    data = json.loads(line)
                    if "messages" in data:
                        f.write(line + '\n')
                        valid_count += 1
                except json.JSONDecodeError:
                    continue
        return valid_count
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}")
        return 0

def main():
    output_file = "raw_dataset.jsonl"
    print("="*60)
    print("BẮT ĐẦU SINH DỮ LIỆU TỰ ĐỘNG QUA GEMINI API (SDK MỚI)")
    print(f"Đầu ra sẽ ghi vào: {output_file}")
    print("="*60)
    
    # Reset file dữ liệu cũ nếu có
    if os.path.exists(output_file):
        os.remove(output_file)
        
    total_generated = 0
    
    # Sinh dữ liệu dịch thuật thuật ngữ IT
    print("\n[Phase 1] Đang sinh dữ liệu dịch thuật IT...")
    for term in it_terms:
        prompt = f"Hãy sinh ra 5 ví dụ hội thoại BrSE (JSONL) xoay quanh việc dịch và giải nghĩa thuật ngữ '{term['ja']}' ({term['vi']}). Người dùng yêu cầu dịch Việt-Nhật, Nhật-Việt hoặc giải thích từ này."
        print(f" -> Đang xử lý thuật ngữ: {term['ja']}")
        count = generate_batch(prompt, output_file)
        total_generated += count
        time.sleep(2) # Giới hạn rate limit API miễn phí
        
    # Sinh dữ liệu email Kính ngữ (Keigo)
    print("\n[Phase 2] Đang sinh dữ liệu email Kính ngữ Keigo...")
    for scenario in communication_scenarios:
        prompt = f"Hãy sinh ra 5 ví dụ hội thoại BrSE (JSONL) trong đó người dùng yêu cầu viết hoặc chuyển đổi một đoạn email sang văn phong Kính ngữ Keigo trang trọng cho tình huống: '{scenario}'."
        print(f" -> Đang xử lý tình huống: {scenario}")
        count = generate_batch(prompt, output_file)
        total_generated += count
        time.sleep(2)
        
    print("\n" + "="*60)
    print(f"HOÀN THÀNH! Tổng cộng đã sinh được {total_generated} dòng dữ liệu hợp lệ.")
    print(f"Tệp tin đã lưu tại: {output_file}")
    print("="*60)

if __name__ == "__main__":
    main()
