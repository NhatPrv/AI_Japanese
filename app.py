import streamlit as st
import requests
import json
import os

# Cấu hình giao diện Streamlit với phong cách Premium Dark Mode
st.set_page_config(
    page_title="AI Bridge Engineer (BrSE) Suite",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS để tạo giao diện Sleek Dark Mode & Glassmorphism cao cấp
st.markdown("""
<style>
    /* Tổng thể nền tối */
    .stApp {
        background-color: #0e1117;
        color: #ecf0f1;
    }
    
    /* Thiết kế Glassmorphism cho các khung chứa */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px rgba(255, 255, 255, 0.08) solid;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    /* Headers đẹp mắt */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-title {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 10px;
    }
    
    /* Style cho các nút bấm */
    .stButton>button {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.5) !important;
    }
    
    /* Style cho vùng nhập dữ liệu */
    .stTextArea textarea {
        background-color: #1a1f29 !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 8px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #0072ff !important;
        box-shadow: 0 0 0 1px #0072ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- HÀM KẾT NỐI OLLAMA API -----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "ja-brse"

def query_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"Lỗi kết nối Ollama (Mã lỗi: {response.status_code})"
    except requests.exceptions.ConnectionError:
        return "LỖI KẾT NỐI: Không thể liên kết tới Ollama Service! Hãy chắc chắn Ollama đang chạy trên máy của bạn (`ollama list` để kiểm tra)."
    except Exception as e:
        return f"Lỗi không xác định: {e}"

# ----------------- GIAO DIỆN WEB APP -----------------

# Sidebar giới thiệu
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/code.png", width=120)
    st.markdown("### AI BrSE Suite v1.0")
    st.markdown("Ứng dụng trợ lý Kỹ sư cầu nối ảo dành riêng cho thị trường IT Nhật Bản.")
    st.divider()
    st.markdown("**Cấu hình cục bộ:**")
    st.info(f"🟢 **Ollama Model**: `{MODEL_NAME}`\n\n🟢 **Platform**: RTX 4060 GPU")
    st.divider()
    st.caption("Phát triển bởi team Antigravity.")

# Tiêu đề chính
st.markdown("<h1 class='main-title'>AI Bridge Engineer Suite</h1>", unsafe_allow_html=True)
st.markdown("##### Soạn thảo email Kính ngữ Keigo và Dịch thuật ngữ IT thông minh bằng mô hình Qwen-2.5-7B fine-tuned.")

# Khởi tạo các Tab
tab1, tab2 = st.tabs(["🌐 Dịch Thuật IT & Giải Nghĩa", "✉️ Soạn Thảo Email Kính Ngữ (Keigo)"])

# ----------------- TAB 1: DỊCH THUẬT & GIẢI NGHĨA IT -----------------
with tab1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Trình dịch thuật thuật ngữ IT thông minh")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_text = st.text_area(
            "Nhập đoạn văn bản cần dịch (Tiếng Việt hoặc Tiếng Nhật):",
            placeholder="Ví dụ: Vui lòng kiểm tra lại môi trường phát triển (development environment) và deploy bản vá lên Production...",
            height=200
        )
        
        btn_translate = st.button("Dịch thuật & Phân tích")
        
    with col2:
        if btn_translate and source_text:
            with st.spinner("Đang phân tích và dịch thuật bằng mô hình Qwen-2.5-7B (GGUF)..."):
                prompt = f"Dịch và giải nghĩa chi tiết các thuật ngữ IT trong đoạn sau: {source_text}"
                translation_result = query_ollama(prompt)
                
                st.markdown("##### 🎯 Kết quả dịch và phân tích thuật ngữ:")
                st.write(translation_result)
        else:
            st.info("Hãy nhập văn bản và nhấn nút 'Dịch thuật' để bắt đầu.")
            
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 2: EMAIL KÍNH NGỮ KEIGO -----------------
with tab2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Trình soạn thảo Email Kính ngữ (Keigo)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        scenario = st.selectbox(
            "Chọn tình huống Email business:",
            [
                "Báo cáo tiến độ dự án bị chậm trễ và xin lỗi đối tác Nhật",
                "Gửi tài liệu thiết kế chi tiết (仕様書) nhờ đối tác review & phản hồi",
                "Giải trình nguyên nhân xảy ra bug nghiêm trọng trên Production & cách khắc phục",
                "Xác nhận đã nhận bàn giao (Delivery) và đang kiểm tra chất lượng",
                "Đặt lịch họp khẩn cấp làm rõ yêu cầu thay đổi (Change Request)",
                "Tùy chỉnh khác..."
            ]
        )
        
        if scenario == "Tùy chỉnh khác...":
            custom_scenario = st.text_input("Nhập tình huống tùy chỉnh của bạn:")
        else:
            custom_scenario = None
            
        sender = st.text_input("Tên của bạn/Công ty:", "Nguyễn Văn A / FPT Software")
        receiver = st.text_input("Tên khách hàng/Đối tác Nhật:", "鈴木様 / 株式会社トヨタ")
        
        key_points = st.text_area(
            "Các ý chính/Lý do (Bằng tiếng Việt):",
            placeholder="Ví dụ: Thiết kế DB bị lỗi, xin trễ hạn 3 ngày. Sẽ họp làm rõ vào ngày mai...",
            height=150
        )
        
        btn_email = st.button("Sinh Email Keigo")
        
    with col2:
        if btn_email and key_points:
            with st.spinner("Đang soạn thảo email Keigo bằng AI..."):
                final_scenario = custom_scenario if custom_scenario else scenario
                prompt = (
                    f"Tình huống email: {final_scenario}\n"
                    f"Người gửi: {sender}\n"
                    f"Người nhận: {receiver}\n"
                    f"Các ý chính cần có trong email: {key_points}\n"
                    f"Hãy viết email Keigo trang trọng gửi khách hàng."
                )
                email_result = query_ollama(prompt)
                
                st.markdown("##### ✉️ Email Business đề xuất (Kèm bản dịch):")
                st.text_area("Kết quả (Bạn có thể copy trực tiếp):", value=email_result, height=350)
        else:
            st.info("Hãy điền các thông tin ý chính bên trái và nhấn nút 'Sinh Email' để bắt đầu.")
            
    st.markdown("</div>", unsafe_allow_html=True)
