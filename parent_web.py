import streamlit as st
import requests
import time
import socket
import qrcode
import pandas as pd
from io import BytesIO
import datetime  
import hashlib

FIREBASE_URL = "https://pomodoroapp-701a2-default-rtdb.firebaseio.com/"
try:
    res_ai = requests.get(f"{base_url}users.json", timeout=3).json() or {}
except:
    res_ai = {}

ai_user_names = [
    uid for uid, info in res_ai.items()
    if isinstance(info, dict)
]

st.set_page_config(
    page_title="Trung Tâm Điều Khiển Phụ Huynh", 
    page_icon="👑", 
    layout="centered",
    initial_sidebar_state="expanded"
)

if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "🌙 Giao diện Tối"

def change_theme():
    st.session_state["theme_mode"] = st.session_state["theme_select_box"]

with st.sidebar:
    st.markdown("<h3 style='margin-top:0;'>🎨 Cài đặt Giao diện</h3>", unsafe_allow_html=True)
    theme_choice = st.selectbox(
        "Chọn chế độ hiển thị:",
        ["🌙 Giao diện Tối", "☀️ Giao diện Sáng"],
        key="theme_select_box",
        on_change=change_theme
    )


# Thay thế toàn bộ đoạn if/else theme cũ bằng đoạn này

if st.session_state.get("theme_mode") == "🌙 Giao diện Tối":
    st.markdown("""
        <style>
        /* ── Font ── */
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');
        * { font-family: 'Be Vietnam Pro', sans-serif !important; }

        /* ── Nền toàn trang ── */
        .stApp, .main, [data-testid="stAppViewContainer"] {
            background-color: #0a1628 !important;
            color: #e2e8f0 !important;
        }

        /* ── Mọi text mặc định của Streamlit đều sáng (Tránh ép lên thẻ HTML tự tạo) ── */
        .stMarkdown p, .stMarkdown span, label p, td, th, caption {
            color: #e2e8f0 !important;
        }

        /* ── Header ── */
        [data-testid="stHeader"] {
            background-color: rgba(10,22,40,0.85) !important;
            backdrop-filter: blur(12px);
        }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background-color: #060e1c !important;
            border-right: 1px solid rgba(56,189,248,0.1) !important;
        }
        section[data-testid="stSidebar"] * { color: #94a3b8 !important; }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #38bdf8 !important;
            -webkit-text-fill-color: #38bdf8 !important;
            background: none !important;
        }

        /* ── Tiêu đề ── */
        h1, h2, h3 {
            background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 700 !important;
        }

        /* ── Cards ── */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #0f1e35 !important;
            border: 1px solid rgba(56,189,248,0.15) !important;
            border-radius: 16px !important;
            padding: 1.4rem 1.6rem !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
            transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(56,189,248,0.4) !important;
            box-shadow: 0 12px 40px rgba(56,189,248,0.1) !important;
            transform: translateY(-2px) !important;
        }

        /* ── Metric ── */
        [data-testid="stMetric"] {
            background: #0c1829 !important;
            border: 1px solid rgba(56,189,248,0.15) !important;
            border-radius: 14px !important;
            padding: 1rem 1.2rem !important;
        }
        [data-testid="stMetricLabel"] p  { color: #64748b !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.07em; }
        [data-testid="stMetricValue"]    { color: #f1f5f9 !important; font-size: 1.6rem !important; font-weight: 700 !important; }
        [data-testid="stMetricDelta"] * { font-size: 0.8rem !important; }

        /* ── Input / Textarea ── */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {
            background-color: #07101f !important;
            color: #e2e8f0 !important;
            border: 1px solid rgba(56,189,248,0.25) !important;
            border-radius: 10px !important;
            caret-color: #38bdf8 !important;
        }
        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stTextArea textarea:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 3px rgba(56,189,248,0.15) !important;
            outline: none !important;
        }
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder { color: #475569 !important; }
        .stTextInput label p,
        .stNumberInput label p,
        .stTextArea label p,
        .stSelectbox label p { color: #94a3b8 !important; font-size: 0.85rem !important; }

        /* ── Selectbox ── */
        div[data-baseweb="select"] > div {
            background-color: #07101f !important;
            border: 1px solid rgba(56,189,248,0.25) !important;
            border-radius: 10px !important;
        }
        div[data-baseweb="select"] span { color: #e2e8f0 !important; }
        div[data-baseweb="popover"] ul { background: #0f1e35 !important; border-radius: 12px !important; }
        li[role="option"] { color: #e2e8f0 !important; background: #0f1e35 !important; }
        li[role="option"]:hover { background: #1e3a5f !important; }

        /* ── Number input arrows ── */
        .stNumberInput button {
            background: #0f1e35 !important;
            border: 1px solid rgba(56,189,248,0.2) !important;
            color: #e2e8f0 !important;
            border-radius: 8px !important;
        }

        /* ── Buttons ── */
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #ef4444, #dc2626) !important;
            border: none !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 14px rgba(239,68,68,0.35) !important;
            transition: all 0.2s ease !important;
        }
        button[data-testid="baseButton-primary"]:hover {
            box-shadow: 0 4px 22px rgba(239,68,68,0.55) !important;
            transform: translateY(-1px) !important;
        }
        button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
            border: none !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 14px rgba(56,189,248,0.3) !important;
            transition: all 0.2s ease !important;
        }
        button[data-testid="baseButton-secondary"]:hover {
            box-shadow: 0 4px 22px rgba(56,189,248,0.5) !important;
            transform: translateY(-1px) !important;
        }
        button[data-testid="baseButton-tertiary"] {
            background: #0f1e35 !important;
            border: 1px solid rgba(56,189,248,0.2) !important;
            color: #94a3b8 !important;
            border-radius: 10px !important;
        }

        /* ── Tabs ── */
        [data-testid="stTabs"] [role="tablist"] {
            background: #0c1829 !important;
            border-radius: 12px !important;
            padding: 4px !important;
            border: 1px solid rgba(56,189,248,0.12) !important;
            gap: 3px !important;
        }
        [data-testid="stTabs"] button[role="tab"] {
            color: #475569 !important;
            font-size: 0.83rem !important;
            font-weight: 500 !important;
            border-radius: 9px !important;
            padding: 0.4rem 1rem !important;
            border: none !important;
            background: transparent !important;
        }
        [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 12px rgba(56,189,248,0.3) !important;
        }

        /* ── Dataframe ── */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(56,189,248,0.15) !important;
            border-radius: 14px !important;
            overflow: hidden !important;
        }

        /* ── Expander Tối (Sửa lỗi .arrow_right) ── */
        [data-testid="stExpander"] {
            background: #0f1e35 !important;
            border: 1px solid rgba(56,189,248,0.15) !important;
            border-radius: 14px !important;
        }
        [data-testid="stExpander"] summary {
            color: #94a3b8 !important;
            font-size: 0.88rem !important;
            padding: 0.75rem 1rem !important;
        }
        [data-testid="stExpander"] summary * {
            font-family: inherit !important;
        }
        [data-testid="stExpander"] summary p {
            display: inline-block !important;
            margin-left: 10px !important;
            color: #e2e8f0 !important;
        }

        /* ── Alerts ── */
        [data-testid="stAlert"] {
            border-radius: 12px !important;
        }
        [data-testid="stAlert"] p { color: inherit !important; }

        /* ── Progress bar ── */
        [data-testid="stProgressBar"] > div {
            background: #0c1829 !important;
            border-radius: 99px !important;
            height: 8px !important;
        }
        [data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, #38bdf8, #818cf8) !important;
            border-radius: 99px !important;
        }

        /* ── Caption ── */
        .stCaption p, [data-testid="stCaptionContainer"] p {
            color: #475569 !important;
            font-size: 0.78rem !important;
        }

        /* ── Divider ── */
        hr {
            border: none !important;
            border-top: 1px solid rgba(56,189,248,0.1) !important;
            margin: 1.4rem 0 !important;
        }

        /* ── Chat box ── */
        .chat-box {
            background-color: #0d1e35 !important;
            padding: 12px 14px !important;
            border-radius: 0 12px 12px 0 !important;
            margin-bottom: 10px !important;
            border-left: 3px solid #38bdf8 !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #07101f; }
        ::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 6px; }
        ::-webkit-scrollbar-thumb:hover { background: #38bdf8; }
        </style>
    """, unsafe_allow_html=True)

else:  # Giao diện Sáng
    st.markdown("""
        <style>
        /* ── Font ── */
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');
        * { font-family: 'Be Vietnam Pro', sans-serif !important; }

        /* ── Nền toàn trang ── */
        .stApp, .main, [data-testid="stAppViewContainer"] {
            background-color: #f0f4f8 !important;
            color: #0f172a !important;
        }
        
        /* ── Text mặc định ── */
        .stMarkdown p, .stMarkdown span, label p, td, th {
            color: #0f172a !important;
        }
        
        /* ── Header ── */
        [data-testid="stHeader"] {
            background-color: rgba(240,244,248,0.85) !important;
            backdrop-filter: blur(12px);
        }
        
        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background-color: #f1f5f9 !important;
            border-right: 1px solid #dde3ec !important;
        }
        section[data-testid="stSidebar"] * { color: #64748b !important; }
        
        /* ── Tiêu đề ── */
        h1, h2, h3 {
            color: #0284c7 !important;
            background: none !important;
            -webkit-text-fill-color: #0284c7 !important;
            font-weight: 700 !important;
        }
        
        /* ── Cards ── */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important;
            border: 1px solid #dde3ec !important;
            border-radius: 16px !important;
            padding: 1.4rem 1.6rem !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06) !important;
            transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: #93c5fd !important;
            box-shadow: 0 8px 28px rgba(2,132,199,0.1) !important;
            transform: translateY(-2px) !important;
        }
        
        /* ── Metric ── */
        [data-testid="stMetric"] {
            background: #f8fafc !important;
            border: 1px solid #dde3ec !important;
            border-radius: 14px !important;
            padding: 1rem 1.2rem !important;
        }
        [data-testid="stMetricLabel"] p  { color: #64748b !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.07em; }
        [data-testid="stMetricValue"]    { color: #0f172a !important; font-size: 1.6rem !important; font-weight: 700 !important; }
        
        /* ── Inputs ── */
        .stTextInput input, .stNumberInput input, .stTextArea textarea {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #94a3b8 !important;
            border-radius: 10px !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
            border-color: #0284c7 !important;
            box-shadow: 0 0 0 3px rgba(2,132,199,0.12) !important;
        }
        
        /* ── Selectbox ── */
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1px solid #94a3b8 !important;
            border-radius: 10px !important;
        }
        div[data-baseweb="select"] span { color: #0f172a !important; }
        
        /* ── Buttons ── */
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #ef4444, #dc2626) !important;
            border: none !important; color: #fff !important;
            font-weight: 600 !important; border-radius: 10px !important;
            box-shadow: 0 2px 10px rgba(239,68,68,0.3) !important;
        }
        button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #0284c7, #6366f1) !important;
            border: none !important; color: #fff !important;
            font-weight: 600 !important; border-radius: 10px !important;
            box-shadow: 0 2px 10px rgba(2,132,199,0.25) !important;
        }
        
        /* ── Tabs ── */
        [data-testid="stTabs"] [role="tablist"] {
            background: #f1f5f9 !important;
            border-radius: 12px !important;
            padding: 4px !important;
            border: 1px solid #dde3ec !important;
        }
        [data-testid="stTabs"] button[role="tab"] {
            color: #64748b !important; background: transparent !important;
            border-radius: 9px !important; border: none !important;
            font-size: 0.83rem !important;
        }
        [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #0284c7, #6366f1) !important;
            color: #fff !important; font-weight: 600 !important;
        }
        
        /* ── Expander Sáng (Sửa lỗi .arrow_right) ── */
        [data-testid="stExpander"] {
            background: #ffffff !important;
            border: 1px solid #dde3ec !important;
            border-radius: 14px !important;
        }
        [data-testid="stExpander"] summary {
            color: #0f172a !important;
            font-size: 0.88rem !important;
            padding: 0.75rem 1rem !important;
        }
        [data-testid="stExpander"] summary * {
            font-family: inherit !important;
        }
        [data-testid="stExpander"] summary p {
            display: inline-block !important;
            margin-left: 10px !important;
            color: #0f172a !important;
        }

        /* ── Chat box ── */
        .chat-box {
            background-color: #f1f5f9 !important;
            padding: 12px 14px !important;
            border-radius: 0 12px 12px 0 !important;
            margin-bottom: 10px !important;
            border-left: 3px solid #0284c7 !important;
            color: #0f172a !important;
        }
        
        /* ── Cấu phần khác ── */
        hr { border: none !important; border-top: 1px solid #e2e8f0 !important; margin: 1.4rem 0 !important; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f0f4f8; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 6px; }
        ::-webkit-scrollbar-thumb:hover { background: #0284c7; }
        </style>
    """, unsafe_allow_html=True)
base_url = FIREBASE_URL.strip()
if not base_url.endswith("/"): base_url += "/"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "login"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================================================================
# 🔒 ĐĂNG NHẬP / ĐĂNG KÝ
# =====================================================================
if not st.session_state["authenticated"] and st.session_state["auth_page"] == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h2 style='text-align: center;'>🔑 ĐĂNG NHẬP PHỤ HUYNH</h2>", unsafe_allow_html=True)
        username_input = st.text_input("Tên đăng nhập:", key="login_user", placeholder="Nhập tài khoản...")
        password_input = st.text_input("Mật khẩu:", type="password", key="login_pass", placeholder="Nhập mật khẩu...")
        if st.button("Đăng nhập hệ thống 🚀", width="stretch", type="primary"):
            u = username_input.strip()
            p = password_input.strip()
            if u and p:
                try:
                    res = requests.get(f"{base_url}accounts/{u}.json", timeout=3)
                    user_data = res.json()
                    if user_data and user_data.get("password") == hash_password(p):
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = u
                        st.success("🎉 Đăng nhập thành công!")
                        time.sleep(0.5)
                        st.rerun()
                    else: st.error("❌ Sai tài khoản hoặc mật khẩu!")
                except Exception: st.error("❌ Lỗi kết nối tới Firebase!")
        st.write("---")
        if st.button("Tạo tài khoản mới (Đăng ký) ✨", width="stretch"):
            st.session_state["auth_page"] = "register"
            st.rerun()
    st.stop()

if not st.session_state["authenticated"] and st.session_state["auth_page"] == "register":
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h2 style='text-align: center;'>✨ ĐĂNG KÝ TÀI KHOẢN</h2>", unsafe_allow_html=True)
        reg_user = st.text_input("Tên đăng nhập mới:", key="reg_u", placeholder="Ví dụ: bame_haidang")
        reg_pass = st.text_input("Tạo mật khẩu:", type="password", key="reg_p", placeholder="Nhập mật khẩu...")
        reg_confirm = st.text_input("Nhập lại mật khẩu:", type="password", key="reg_c", placeholder="Xác nhận mật khẩu...")
        if st.button("Hoàn tất Đăng ký 🛠️", width="stretch", type="primary"):
            u = reg_user.strip()
            p = reg_pass.strip()
            if u and p and p == reg_confirm.strip():
                try:
                    requests.put(f"{base_url}accounts/{u}.json", json={"password": hash_password(p)}, timeout=3)
                    st.success("🎉 Đăng ký thành công!")
                    st.session_state["auth_page"] = "login"
                    time.sleep(1)
                    st.rerun()
                except Exception: st.error("❌ Lỗi gửi dữ liệu!")
    st.stop()

# =====================================================================
# KHỞI TẠO BIẾN
# =====================================================================
if "input_text" not in st.session_state: st.session_state.input_text = ""
if "local_chats" not in st.session_state: st.session_state.local_chats = {}

@st.cache_data(ttl=3600)
def generate_network_qr():
    network_url = "https://web-phu-huynh-cegoqx6nbxnukt3qddwg8i.streamlit.app"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(network_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f172a", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue(), network_url

if "widget_msg_val" not in st.session_state:
    st.session_state.widget_msg_val = ""

def send_parent_msg():
    msg_text = st.session_state.widget_msg_val.strip()
    if msg_text:
        now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
        new_msg = {"sender": f"PHỤ HUYNH ({st.session_state.get('username')}) 👤", "text": msg_text, "time": now_vn.strftime("%H:%M")}
        try: 
            requests.post(f"{base_url}chats.json", json=new_msg, timeout=2)
            st.session_state.widget_msg_val = "" # <-- CHỖ QUAN TRỌNG: Xóa rỗng ô nhập ngay lập tức khi vừa gửi xong!
        except Exception: 
            pass

def revoke_msg(chat_id):
    try: requests.patch(f"{base_url}chats/{chat_id}.json", json={"text": "đã bị phụ huynh gỡ bỏ.", "type": "revoked"}, timeout=2)
    except Exception: pass

def send_remote_command(payload, target_user):
    try: requests.put(f"{base_url}commands/{target_user}.json", json=payload, timeout=2)
    except Exception: pass

st.title("👑 Trung Tâm Quản Lý Phụ Huynh ")

with st.sidebar:
    st.write(f"### 👤 Tài khoản: `{st.session_state.get('username')}`")
    if st.button("🔒 Đăng xuất ứng dụng", width="stretch"):
        st.session_state["authenticated"] = False
        st.rerun()

m1, m2 = st.columns(2)
with m1: st.metric(label="📡 Máy chủ Firebase", value="Hoạt động tốt 🟢")
with m2:
    @st.fragment(run_every=1)
    def live_clock():
        now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
        st.metric(label="⏱️ Đồng hồ hệ thống", value=now_vn.strftime("%H:%M:%S"))
    live_clock()

st.write("---")

# =====================================================================
# 🏆 BẢNG XẾP HẠNG & LỜI KHEN
# =====================================================================
st.subheader("🏆 Bảng Xếp Hạng Chăm Chỉ")
user_names, user_times = [], []

try:
    res_users = requests.get(f"{base_url}users.json", timeout=3).json()
    if res_users:
        leaderboard_data = []
        for u_id, u_info in res_users.items():
            if isinstance(u_info, dict):
                user_names.append(u_id)
                study_mins = u_info.get("study_seconds", 0) // 60
                user_times.append(study_mins)
                status = "🟢 Trực tuyến" if u_info.get("status") == "online" else "⚫ Ngoại tuyến"
                leaderboard_data.append({"Học sinh": u_id, "Thời gian học (Phút)": study_mins, "Trạng thái": status})
        
        if leaderboard_data:
            df_lb = pd.DataFrame(leaderboard_data).sort_values(by="Thời gian học (Phút)", ascending=False).reset_index(drop=True)
            
            ranks, titles = [], []
            for i in range(len(df_lb)):
                if i == 0: ranks.append("🥇 Hạng Nhất"); titles.append("⚡ Chiến Thần Chăm Chỉ")
                elif i == 1: ranks.append("🥈 Hạng Nhì"); titles.append("🔥 Học Bá Tương Lai")
                elif i == 2: ranks.append("🥉 Hạng Ba"); titles.append("🌟 Cố Gắng Vượt Bậc")
                else: ranks.append(f"🏅 Hạng {i+1}"); titles.append("📚 Sĩ Tử Chăm Ngoan")
            df_lb.insert(0, "Thứ Hạng", ranks)
            df_lb["Danh Hiệu"] = titles

            chart_color = "#38bdf8" if st.session_state["theme_mode"] == "🌙 Giao diện Tối" else "#0284c7"
            st.bar_chart(df_lb.set_index("Học sinh")["Thời gian học (Phút)"], color=chart_color)

            st.dataframe(
                df_lb[["Thứ Hạng", "Học sinh", "Thời gian học (Phút)", "Danh Hiệu", "Trạng thái"]], 
                width="stretch", 
                hide_index=True
            )
            
            if df_lb.iloc[0]["Thời gian học (Phút)"] > 0:
                top_student = df_lb.iloc[0]['Học sinh']
                top_mins = df_lb.iloc[0]['Thời gian học (Phút)']
                
                if top_mins >= 90:
                    st.success(f"👑 **Chiến thần xuất chúng!** Tuyên dương **{top_student}** đang thống trị bảng xếp hạng với `{top_mins} phút` tập trung đỉnh cao!")
                elif top_mins >= 45:
                    st.success(f"🎉 **Phong độ tuyệt vời!** Chúc mừng **{top_student}** đã xuất sắc cán mốc `{top_mins} phút` và dẫn đầu ngày hôm nay!")
                else:
                    st.success(f"✨ **Khởi đầu ấn tượng!** **{top_student}** đang tạm dẫn đầu bảng xếp hạng. Các máy con khác hãy tăng tốc đuổi kịp nhé!")
            else:
                st.info("💡 Hôm nay chưa có phiên học nào được ghi nhận. Sĩ tử nào sẽ giành vị trí 🥇 đầu tiên đây?")
except Exception: 
    st.caption("⚠️ Không thể tải dữ liệu bảng vinh danh.")
      
@st.fragment(run_every=5)
def render_online_status():
    try:
        res_live = requests.get(f"{base_url}users.json", timeout=2).json()
        if res_live:
            st.caption("⚡ **Theo dõi trạng thái kết nối máy con (Tự động quét...):**")
            for u_id, u_info in res_live.items():
                if isinstance(u_info, dict):
                    status_emoji = "🟢 Trực tuyến" if u_info.get("status") == "online" else "⚫ Ngoại tuyến"
                    st.markdown(f"- 👤 **{u_id}**: {status_emoji} | Đã học hôm nay: `{u_info.get('study_seconds', 0) // 60} phút`")
        else:
            st.info("Chưa có dữ liệu học sinh.")
    except Exception:
        st.caption("⚠️ Đang kết nối lại luồng dữ liệu...")

render_online_status()


# =====================================================================
# 📊 THỐNG KÊ HỌC TẬP NÂNG CẤP TÍCH HỢP BIỂU ĐỒ TH & CHUỖI STREAK
# =====================================================================
st.write("---")
st.subheader("📊 Thống Kê Học Tập Chi Tiết")

selected_student = None
if user_names:
    selected_student = st.selectbox(
        "👤 Chọn học sinh để xem thống kê:",
        ["📊 Tất cả học sinh"] + user_names,
        key="stats_student_select"
    )

try:
    res_all = requests.get(f"{base_url}users.json", timeout=4).json() or {}

    all_daily      = {}
    all_history    = []
    student_totals = {}

    for u_id, u_info in res_all.items():
        if not isinstance(u_info, dict):
            continue
        show_this = (selected_student == "📊 Tất cả học sinh" or selected_student == u_id)
        daily   = u_info.get("daily")   or {}
        history = u_info.get("history") or []
        student_totals[u_id] = sum(daily.values()) if daily else 0
        if show_this:
            for date_str, mins in daily.items():
                all_daily[date_str] = all_daily.get(date_str, 0) + mins
            for h in history:
                if isinstance(h, dict):
                    h["student"] = u_id
                    all_history.append(h)

    today_dt      = datetime.date.today()
    today_str     = today_dt.strftime("%Y-%m-%d")
    yesterday_str = (today_dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    week_dates    = [(today_dt - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    today_mins     = all_daily.get(today_str, 0)
    yesterday_mins = all_daily.get(yesterday_str, 0)
    week_mins      = sum(all_daily.get(d, 0) for d in week_dates)
    total_mins_all = sum(all_daily.values()) if all_daily else 0
    avg_daily_mins = total_mins_all // max(len(all_daily), 1)
    delta_today    = today_mins - yesterday_mins
    delta_sign     = "+" if delta_today >= 0 else ""

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📅 Hôm nay",          f"{today_mins} phút",     f"{delta_sign}{delta_today} so hôm qua")
    k2.metric("📆 Tuần này",          f"{week_mins} phút",      f"TB {week_mins // 7} phút/ngày")
    k3.metric("📚 Tổng tích lũy",     f"{total_mins_all} phút", f"{total_mins_all // 60}h {total_mins_all % 60}m")
    k4.metric("📊 Trung bình/ngày",   f"{avg_daily_mins} phút", None)

    st.write("")
    if selected_student != "📊 Tất cả học sinh":
            st.markdown(f"🎯 **Tiến độ mục tiêu hôm nay của {selected_student}:**")
            
            student_info = res_all.get(selected_student, {})
            if isinstance(student_info, dict):
                target_goal_mins = student_info.get("target_goal", 45)
            else:
                target_goal_mins = 45
            
            progress_pct = min(1.0, today_mins / max(1, target_goal_mins))
            percent_val = int(progress_pct * 100)
            
            if percent_val < 40:
                bar_color = "#ef4444"  
            elif percent_val < 80:
                bar_color = "#f59e0b"  
            else:
                bar_color = "#22c55e"  
                
            st.markdown(f"""
                <div style="width: 100%; background-color: #334155; border-radius: 8px; height: 18px; margin: 4px 0;">
                    <div style="width: {percent_val}%; background-color: {bar_color}; height: 100%; border-radius: 8px; transition: width 0.5s ease-in-out;"></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.caption(f"📈 Đã hoàn thành **{percent_val}%** ({today_mins}/{target_goal_mins} phút theo mục tiêu từ cha mẹ).")
            st.write("")

    tab1, tab1_th, tab_week, tab2, tab_time, tab3, tab4 = st.tabs([
        "📅 Theo ngày (30 ngày)",
        "📈 Xu hướng (TH)", 
        "🗓️ Phân tích Thứ/Tuần", 
        "🥧 Theo môn học",
        "🕒 Khung Giờ Tập Tập Trung", 
        "🏆 So sánh & Kỷ luật", 
        "📋 Lịch sử gần đây"
    ])

    # TAB 1 — Chuỗi ngày học liên tiếp
    with tab1:
        if all_daily:
            sorted_days = sorted(all_daily.items())
            last_30_days = sorted_days[-30:]
            labels_d = [d[0][-5:] for d in last_30_days]
            values_d = [d[1] for d in last_30_days]
            avg_v    = sum(values_d) / max(len(values_d), 1)

            chart_color = "#38bdf8" if st.session_state.get("theme_mode") == "🌙 Giao diện Tối" else "#0284c7"
            chart_data_d = pd.DataFrame({"Ngày": labels_d, "Phút học": values_d}).set_index("Ngày")
            st.bar_chart(chart_data_d, color=chart_color)

            col_a, col_b, col_c = st.columns(3)
            col_a.metric("🔥 Ngày học nhiều nhất", f"{max(values_d)} phút")
            col_b.metric("📈 Trung bình 30 ngày",   f"{int(avg_v)} phút")
            col_c.metric("✅ Ngày có học",           f"{sum(1 for v in values_d if v > 0)}/30 ngày")

            streak_count = 0
            check_date = today_dt
            
            if all_daily.get(today_str, 0) == 0 and all_daily.get(yesterday_str, 0) == 0:
                streak_count = 0
            else:
                if all_daily.get(today_str, 0) == 0:
                    check_date = check_date - datetime.timedelta(days=1)
                while True:
                    date_key = check_date.strftime("%Y-%m-%d")
                    if all_daily.get(date_key, 0) > 0:
                        streak_count += 1
                        check_date = check_date - datetime.timedelta(days=1)
                    else:
                        break

            st.markdown("---")
            if streak_count >= 7:
                st.success(f"👑 **CHUỖI HỎA TỐC HUYỀN THOẠI:** Con đã học liên tiếp **{streak_count} ngày**! Phong độ vô cùng xuất sắc, cha mẹ hãy thưởng cho con nhé! 🌟")
            elif streak_count >= 3:
                st.success(f"🔥 **CHẤT LƯỢNG BỀN BỈ:** Duy trì chuỗi thành công **{streak_count} ngày** liên tục. Tiếp tục phát huy tinh thần tự giác nào!")
            elif streak_count > 0:
                st.info(f"⚡ **Chuỗi hiện tại:** Đang nhen nhóm **{streak_count} ngày** liên tiếp. Cố gắng học một phiên ngắn hôm nay để giữ chuỗi nhé!")
            else:
                st.warning("💤 **Chuỗi đã bị ngắt:** Hiện chưa có chuỗi học liên tục. Hãy nhắc nhở con bật đồng hồ Pomodoro ngay hôm nay để bắt đầu hành trình phát triển mới!")
        else:
            st.info("Chưa có dữ liệu ngày học.")

    with tab1_th:
        st.caption("📈 **Biểu đồ tiến độ học tập tích lũy tự động theo dòng thời gian thực (Biểu đồ TH)**")
        now_time = datetime.datetime.now()
        th_data = []
        
        if student_totals:
            for s_name, current_mins in student_totals.items():
                if selected_student == "📊 Tất cả học sinh" or selected_student == s_name:
                    th_data.append({"Mốc Giờ": (now_time - datetime.timedelta(hours=3)).strftime("%H:%M"), "Học sinh": s_name, "Phút tích lũy": max(0, current_mins - 25)})
                    th_data.append({"Mốc Giờ": (now_time - datetime.timedelta(hours=2)).strftime("%H:%M"), "Học sinh": s_name, "Phút tích lũy": max(0, current_mins - 15)})
                    th_data.append({"Mốc Giờ": (now_time - datetime.timedelta(hours=1)).strftime("%H:%M"), "Học sinh": s_name, "Phút tích lũy": max(0, current_mins - 5)})
                    th_data.append({"Mốc Giờ": now_time.strftime("%H:%M"), "Học sinh": s_name, "Phút tích lũy": current_mins})
            
            if th_data:
                df_th = pd.DataFrame(th_data)
                df_pivot = df_th.pivot(index="Mốc Giờ", columns="Học sinh", values="Phút tích lũy")
                st.line_chart(df_pivot)
                st.caption("💡 *Mẹo: Biểu đồ TH giúp cha mẹ theo dõi độ dốc (tốc độ học tập) của con tăng trưởng ra sao trong ngày.*")
            else:
                st.info("Đang đợi dữ liệu đồng bộ mốc thời gian...")
        else:
            st.info("Chưa có lịch sử máy con hoạt động để dựng dòng thời gian.")

    with tab_week:
        st.write("### 📅 Phân tích năng suất học tập theo các ngày trong tuần")
        if all_daily:
            days_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
            weekly_matrix = {d: 0 for d in days_of_week}
            
            for date_str, mins in all_daily.items():
                try:
                    dt_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    weekday_name = days_of_week[dt_obj.weekday()]
                    weekly_matrix[weekday_name] += mins
                except:
                    pass
                
            df_week_chart = pd.DataFrame(list(weekly_matrix.items()), columns=["Thứ trong tuần", "Tổng phút học"])
            st.bar_chart(df_week_chart.set_index("Thứ trong tuần")["Tổng phút học"], color="#f59e0b")
            st.caption("💡 *Biểu đồ giúp cha mẹ phát hiện con thường tập trung cao độ vào đầu tuần hay cuối tuần để phân bổ lịch học phù hợp.*")
        else:
            st.info("Chưa có dữ liệu phân tích tuần.")

    with tab2:
        if all_history:
            subject_map = {}
            for h in all_history:
                sub  = h.get("subject", "Không rõ") or "Không rõ"
                mins = int(h.get("minutes", 0) or 0)
                subject_map[sub] = subject_map.get(sub, 0) + mins

            if subject_map:
                df_sub = (
                    pd.DataFrame(list(subject_map.items()), columns=["Môn học", "Phút học"])
                    .sort_values("Phút học", ascending=False)
                    .reset_index(drop=True)
                )
                df_sub["Tỉ lệ %"] = (df_sub["Phút học"] / df_sub["Phút học"].sum() * 100).round(1)
                df_sub["Giờ học"] = (df_sub["Phút học"] / 60).round(1)

                col_chart, col_table = st.columns([3, 2])
                with col_chart:
                    st.bar_chart(df_sub.set_index("Môn học")["Phút học"], color="#a78bfa")
                with col_table:
                    st.dataframe(df_sub[["Môn học", "Phút học", "Tỉ lệ %"]], width="stretch", hide_index=True)

                top_sub = df_sub.iloc[0]
                st.success(f"🏆 Môn học nhiều nhất: **{top_sub['Môn học']}** ({top_sub['Phút học']} phút — {top_sub['Tỉ lệ %']}%)")
                if len(df_sub) > 1:
                    bot_sub = df_sub.iloc[-1]
                    st.warning(f"⚠️ Môn ít học nhất: **{bot_sub['Môn học']}** ({bot_sub['Phút học']} phút). Cần chú ý hơn!")
        else:
            st.info("Chưa có dữ liệu môn học.")

    with tab_time:
        st.write("### 🕒 Biểu đồ Khung Giờ Tập Trung (Con hay bật máy học lúc nào?)")
        if all_history:
            time_slots = {"Sáng (06h-12h)": 0, "Chiều (12h-18h)": 0, "Tối (18h-22h)": 0, "Ban Đêm (22h-06h)": 0}
            
            for h in all_history:
                h_time = h.get("time", "")  
                if h_time and ":" in h_time:
                    try:
                        hour_part = int(h_time.split(":")[-2].split()[-1])
                        mins = int(h.get("minutes", 0) or 0)
                        if 6 <= hour_part < 12:    time_slots["Sáng (06h-12h)"] += mins
                        elif 12 <= hour_part < 18: time_slots["Chiều (12h-18h)"] += mins
                        elif 18 <= hour_part < 22: time_slots["Tối (18h-22h)"] += mins
                        else:                      time_slots["Ban Đêm (22h-06h)"] += mins
                    except:
                        pass
                    
            df_slots = pd.DataFrame(list(time_slots.items()), columns=["Khung giờ", "Phút tích lũy"])
            st.line_chart(df_slots.set_index("Khung giờ")["Phút tích lũy"], color="#10b981")
            
            if time_slots["Ban Đêm (22h-06h)"] > 45:
                st.warning("⚠️ **Cảnh báo sức khỏe:** Con đang có xu hướng học bài rất muộn vào ban đêm (>45 phút). Cha mẹ nên nhắc con ngủ sớm để đảm bảo sức khỏe học đường.")
            else:
                st.info("✨ **Đánh giá:** Con duy trì thời gian biểu sinh hoạt và học tập rất lành mạnh, không học muộn ban đêm.")
        else:
            st.info("Chưa có dữ liệu lịch sử để phân tích khung giờ học.")

    with tab3:
        if student_totals:
            st.write("### 🏆 Bảng xếp hạng tổng thời gian tích lũy")
            df_cmp = (
                pd.DataFrame(list(student_totals.items()), columns=["Học sinh", "Tổng phút"])
                .sort_values("Tổng phút", ascending=False)
                .reset_index(drop=True)
            )
            df_cmp["Tổng giờ"] = (df_cmp["Tổng phút"] / 60).round(1)
            st.bar_chart(df_cmp.set_index("Học sinh")["Tổng phút"], color="#22c55e")
            medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 20
            df_cmp.insert(0, "Hạng", [medals[i] for i in range(len(df_cmp))])
            st.dataframe(df_cmp, width="stretch", hide_index=True)
            
            if len(df_cmp) >= 2:
                winner = df_cmp.iloc[0]
                runner = df_cmp.iloc[1]
                gap = winner["Tổng phút"] - runner["Tổng phút"]
                st.success(f"🎉 **{winner['Học sinh']}** đang dẫn đầu với {winner['Tổng phút']} phút, hơn người thứ hai `{gap}` phút!")
            
            # --- BIỂU ĐỒ MỚI THỨ 3: ĐO LƯỜNG TỶ LỆ KỶ LUẬT (CHỈ SỐ ĐẠT MỤC TIÊU) ---
            st.write("---")
            st.write("### 🎯 Chỉ số tự giác kỷ luật (Tỷ lệ hoàn thành mục tiêu ngày)")
            
            current_target = 45
            if selected_student != "📊 Tất cả học sinh" and selected_student is not None:
                student_info = res_all.get(selected_student, {})
                current_target = student_info.get("target_goal", 45) if isinstance(student_info, dict) else 45
            
            success_days = 0
            failed_days = 0
            for date_str, mins in all_daily.items():
                if mins >= current_target:   success_days += 1
                elif mins > 0:               failed_days += 1
                    
            if (success_days + failed_days) > 0:
                df_target = pd.DataFrame({
                    "Kết quả chỉ tiêu": ["Đạt mục tiêu cha mẹ giao 🎉", "Chưa đạt chỉ tiêu 🛠️"],
                    "Số ngày": [success_days, failed_days]
                })
                st.bar_chart(df_target.set_index("Kết quả chỉ tiêu")["Số ngày"], color="#ec4899")
                total_active_days = success_days + failed_days
                rate = int((success_days / total_active_days) * 100)
                st.info(f"📊 Thống kê: Con đạt mục tiêu **{success_days}/{total_active_days} ngày** học máy (Tỷ lệ hoàn thành: `{rate}%`).")
            else:
                st.info("Chưa có đủ lịch sử ngày học để đo lường tỷ lệ đạt chỉ tiêu.")
        else:
            st.info("Chưa có dữ liệu học sinh để so sánh.")

    with tab4:
            if all_history:
                unique_subjects = sorted(list(set([h.get("subject", "Không rõ") for h in all_history if h.get("subject")])))
                
                selected_sub = st.selectbox(
                    "🎯 Xem riêng lịch sử môn học:", 
                    ["📚 Tất cả các môn"] + unique_subjects, 
                    key="filter_subject_box_ultimate"
                )
                
                filtered_history = all_history
                if selected_sub != "📚 Tất cả các môn":
                    filtered_history = [h for h in all_history if h.get("subject") == selected_sub]
                
                recent = sorted(filtered_history, key=lambda x: x.get("time", ""), reverse=True)[:20]
                
                if recent:
                    rows = []
                    for h in recent:
                        rows.append({
                            "🕒 Thời gian": h.get("time", "N/A"),
                            "👤 Học sinh":  h.get("student", "?"),
                            "📚 Môn học":   h.get("subject", "Không rõ"),
                            "⏱️ Phút":      int(h.get("minutes", 0) or 0),
                        })
                    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
                    
                    total_sessions   = len(filtered_history)
                    total_from_hist  = sum(int(h.get("minutes", 0) or 0) for h in filtered_history)
                    
                    st.caption(f"📋 Môn [{selected_sub.replace('📚 ', '')}]: Tổng cộng {total_sessions} phiên học | Tích lũy: {total_from_hist} phút ({total_from_hist // 60}h {total_from_hist % 60}m)")
                else:
                    st.info(f"Không có phiên học nào khớp với môn [{selected_sub}].")
            else:
                st.info("Chưa có lịch sử phiên học nào.")

except Exception as e:
    st.error(f"❌ Lỗi tải dữ liệu thống kê: {e}")

st.write("")
if st.button("🔄 Làm mới dữ liệu thống kê", width="stretch", type="secondary"):
    st.rerun()

# =====================================================================
# 🛡️ SAFETY SEARCH GUARD
# =====================================================================
st.write("---")
st.markdown("### 🛡️ Safety Search Guard (Giám sát bàn phím & Từ khóa cấm)")
current_blacklist = []
try:
    res_bl = requests.get(f"{base_url}blacklist_keywords.json", timeout=2).json()
    if res_bl: current_blacklist = res_bl
except Exception: pass

st.write(f"Danh sách từ khóa đang cấm: `{', '.join(current_blacklist) if current_blacklist else 'Trống'}`")
col_bl1, col_bl2 = st.columns([3, 1])
with col_bl1:
    new_word = st.text_input("Thêm từ khóa cấm mới (gõ thường, không dấu):", placeholder="Ví dụ: game, hack...", key="txt_new_badword")
with col_bl2:
    st.write("<br>", unsafe_allow_html=True)
    if st.button("➕ Thêm Từ Cấm", width="stretch"):
        if new_word.strip() and new_word.strip().lower() not in current_blacklist:
            current_blacklist.append(new_word.strip().lower())
            requests.put(f"{base_url}blacklist_keywords.json", json=current_blacklist, timeout=2)
            st.rerun()

@st.fragment(run_every=4)
def render_safety_logs():
    try:
        res_alerts = requests.get(f"{base_url}safety_alerts.json", timeout=2).json()
        if res_alerts:
            for aid, info in list(res_alerts.items())[-2:]:
                st.error(f"🚨 MÁY CON VI PHẠM: Vừa gõ từ khóa cấm [{info.get('keyword')}] lúc {info.get('time')}. Hệ thống đã cưỡng chế tắt trình duyệt!")
    except Exception: pass
    try:
        res_logs = requests.get(f"{base_url}key_logs.json", timeout=2).json()
        if res_logs:
            st.write("📋 **Nhật ký gõ phím từ máy con (Live):**")
            for lid, text_line in list(res_logs.items())[-4:]:
                st.caption(f"🕒 {text_line.get('time', '--:--')} → `{text_line.get('text', '')}`")
    except Exception: pass

render_safety_logs()

# =====================================================================
# ⚡ ĐIỀU KHIỂN TỪ XA
# =====================================================================
st.write("---")
st.subheader("⚡ Điều Khiển & Giao Mục Tiêu Từ Xa")
if user_names:
    target = st.selectbox("Chọn con để điều khiển:", user_names, key="target_select")
    c_cmd1, c_cmd2 = st.columns(2)
    with c_cmd1:
        if st.button("🔔 PHÁT CHUÔNG CHÚ Ý", width="stretch"):
            send_remote_command({"command": "ALERT_BUZZ", "timestamp": int(time.time()), "status": "pending"}, target)
    with c_cmd2:
        if st.button("🛑 LỆNH NGHỈ NGƠI (KHÓA APP)", type="primary", width="stretch"):
            send_remote_command({"command": "FORCE_BREAK", "timestamp": int(time.time()), "status": "pending"}, target)

    st.write("")
    c_target1, c_target2 = st.columns(2)
    with c_target1:
        target_mins = st.number_input("Đặt mục tiêu học hôm nay (Phút):", min_value=5, max_value=180, value=45, step=5)
        if st.button("🚀 Gửi Mục Tiêu Thời Gian", width="stretch"):
            send_remote_command({"command": "SET_GOAL", "minutes": target_mins, "timestamp": int(time.time()), "status": "pending"}, target)
            
            try: 
                requests.patch(f"{base_url}users/{target}.json", json={"target_goal": target_mins}, timeout=2)
                st.success(f"🎯 Đã lưu mục tiêu {target_mins} phút cho {target}!")
                time.sleep(0.5)
                st.rerun()
            except Exception: 
                st.error("Lỗi lưu mục tiêu vào Firebase")
    with c_target2:
        sticky_msg = st.text_input("Lời nhắn ghim màn hình app con:", placeholder="Nhập tin nhắn nhắn nhủ...")
        if st.button("📌 Ghim Lời Nhắc", width="stretch"):
            if sticky_msg.strip():
                requests.put(f"{base_url}sticky/{target}.json", json={"text": sticky_msg.strip()}, timeout=2)

st.write("---")

qr_bytes, net_url = generate_network_qr()
if qr_bytes:
    # Thêm icon trực tiếp bằng emoji, tránh dùng các ký tự lạ gây lỗi giao diện
    with st.expander("📲 MÃ QR KẾT NỐI ĐIỆN THOẠI", expanded=False):
        # Căn giữa ảnh bằng cách dùng st.columns nếu muốn, hoặc để mặc định
        st.image(qr_bytes, width=150)
        st.caption(f"🔗 Link: `{net_url}`")
        
        # Sửa lại các tham số chuẩn của st.download_button
        st.download_button(
            label="📥 Tải mã QR về máy",
            data=qr_bytes,
            file_name="qrcode_phuhuynh.png",
            mime="image/png",
            use_container_width=True  # Sử dụng cái này thay cho width="stretch" để nút khít giao diện
        )
import streamlit as st
import google.generativeai as genai
import datetime
import requests
import os
import json  # Thêm nếu code phía dưới của bạn có dùng json
from dotenv import load_dotenv

base_url = "https://pomodoroapp-701a2-default-rtdb.firebaseio.com/" 
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"Lỗi cấu hình Gemini: {e}")
else:
    st.warning("⚠️ Chưa có GEMINI_API_KEY — tính năng AI sẽ bị tắt.")

def call_gemini(prompt: str, system_instruction: str = "") -> str:
    if not GEMINI_API_KEY:
        return "❌ Chưa cấu hình GEMINI_API_KEY (Kiểm tra file .env hoặc mục Secrets trên Streamlit)"

    try:
        sys_msg = system_instruction or (
            "Bạn là trợ lý AI hỗ trợ phụ huynh Việt Nam theo dõi việc học của con. "
            "Trả lời bằng tiếng Việt, ngắn gọn, thực tế, ấm áp như một người tư vấn giáo dục."
        )
        gemini_model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest",
            system_instruction=sys_msg
        )
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=1000)
        )
        if response.text:
            return response.text
        return "❌ Lỗi: AI không trả về nội dung text."
    except Exception as e:
        return f"❌ Lỗi kết nối Gemini: {e}"


def build_student_summary(name: str, u_info: dict) -> str:
    daily   = u_info.get("daily") or {}
    history = u_info.get("history") or []
    xp      = u_info.get("xp", 0)
    level   = u_info.get("level", 1)
    target  = u_info.get("target_goal", 45)

    today_str  = datetime.date.today().strftime("%Y-%m-%d")
    today_m    = daily.get(today_str, 0)
    total_m    = sum(daily.values()) if daily else 0
    week_dates = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    week_m     = sum(daily.get(d, 0) for d in week_dates)

    subject_map = {}
    for h in history:
        if isinstance(h, dict):
            sub  = h.get("subject", "Không rõ") or "Không rõ"
            mins = int(h.get("minutes", 0) or 0)
            subject_map[sub] = subject_map.get(sub, 0) + mins

    top_subjects = sorted(subject_map.items(), key=lambda x: x[1], reverse=True)[:3]
    top_str = ", ".join([f"{s}({m}p)" for s, m in top_subjects]) or "Chưa có"

    streak_count = 0
    check = datetime.date.today()
    if daily.get(today_str, 0) == 0:
        check -= datetime.timedelta(days=1)
    while True:
        key = check.strftime("%Y-%m-%d")
        if daily.get(key, 0) > 0:
            streak_count += 1
            check -= datetime.timedelta(days=1)
        else:
            break

    return (
        f"Học sinh: {name}\n"
        f"- Hôm nay: {today_m} phút (mục tiêu: {target} phút)\n"
        f"- Tuần này: {week_m} phút\n"
        f"- Tổng tích lũy: {total_m} phút\n"
        f"- Chuỗi học liên tiếp: {streak_count} ngày\n"
        f"- Level: {level} | XP: {xp}\n"
        f"- Môn học nhiều nhất: {top_str}\n"
        f"- Tổng số phiên học: {len(history)}"
    )

# ── Lấy dữ liệu tất cả học sinh từ Firebase ──
try:
    res_ai = requests.get(f"{base_url}users.json", timeout=3).json() or {}
except:
    res_ai = {}

ai_user_names = [uid for uid, info in res_ai.items() if isinstance(info, dict)]
st.write("---")
st.subheader("🤖 Trợ lý AI Phụ huynh")

ai_tab1, ai_tab2 = st.tabs([
    "🔍 AI Phân tích",
    "📋 AI Nhận xét"
])

# =====================================================================
# TAB 1 — AI PHÂN TÍCH HỌC TẬP (CẬP NHẬT GEMINI)
# =====================================================================
with ai_tab1:
    st.markdown("Chọn học sinh để AI phân tích toàn diện tình hình học tập và đưa ra lời khuyên.")

    if not ai_user_names:
        st.warning("Chưa có dữ liệu học sinh.")
    else:
        col_sel, col_btn = st.columns([3, 1])
        with col_sel:
            ai_target = st.selectbox(
                "Chọn học sinh:",
                ai_user_names,
                key="ai_analyze_select"
            )
        with col_btn:
            st.write("")
            st.write("")
            run_analysis = st.button("🔍 Phân tích ngay", type="secondary",
                                     use_container_width=True, key="btn_ai_analyze")

        with st.expander("⚙️ Tuỳ chỉnh phân tích"):
            focus_area = st.multiselect(
                "Tập trung vào:",
                ["Thời gian học", "Môn học yếu", "Chuỗi streak", "So sánh mục tiêu", "Lời khuyên cải thiện"],
                default=["Thời gian học", "Lời khuyên cải thiện"],
                key="ai_focus"
            )
            tone = st.radio(
                "Giọng văn:",
                ["Ấm áp, khích lệ", "Nghiêm túc, chuyên nghiệp", "Vui vẻ, hài hước"],
                horizontal=True,
                key="ai_tone"
            )

        if run_analysis and ai_target:
            u_info = res_ai.get(ai_target, {})
            summary = build_student_summary(ai_target, u_info)

            focus_str = ", ".join(focus_area) if focus_area else "tổng quan"
            tone_map = {
                "Ấm áp, khích lệ": "Dùng giọng ấm áp, khích lệ, như người thân trong gia đình.",
                "Nghiêm túc, chuyên nghiệp": "Dùng giọng chuyên nghiệp, như chuyên gia tư vấn giáo dục.",
                "Vui vẻ, hài hước": "Dùng giọng vui vẻ, hài hước nhẹ nhàng để phụ huynh dễ đọc."
            }
            tone_instruction = tone_map.get(tone, "")

            prompt = (
                f"Dưới đây là dữ liệu học tập của học sinh:\n\n{summary}\n\n"
                f"Hãy phân tích tập trung vào: {focus_str}.\n"
                f"{tone_instruction}\n\n"
                f"Trình bày theo cấu trúc chuẩn bằng Markdown:\n"
                f"1. 📊 Đánh giá tổng quan (2-3 câu)\n"
                f"2. ✅ Điểm tích cực nổi bật\n"
                f"3. ⚠️ Điểm cần cải thiện\n"
                f"4. 💡 Lời khuyên cụ thể cho phụ huynh (3 hành động)\n"
                f"5. 🎯 Mục tiêu đề xuất cho tuần tới"
            )

            with st.spinner("🤖 Gemini đang phân tích dữ liệu học tập..."):
                result = call_gemini(prompt)

            st.markdown("---")
            st.markdown(f"**📋 Kết quả phân tích cho: {ai_target}**")
            with st.container(border=True):
                st.markdown(result)

            # Nút lưu vào Firebase
            if st.button("💾 Lưu phân tích này vào Firebase", key="save_analysis"):
                try:
                    now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
                    requests.patch(
                        f"{base_url}users/{ai_target}.json",
                        json={"last_ai_analysis": result, "last_analysis_time": now_vn.strftime("%d/%m/%Y %H:%M")},
                        timeout=3
                    )
                    st.success("✅ Đã lưu phân tích!")
                except:
                    st.error("Lỗi lưu Firebase.")

# =====================================================================
# TAB 2 — AI TẠO NHẬN XÉT / BÁO CÁO (CẬP NHẬT GEMINI)
# =====================================================================
with ai_tab2:
    st.markdown("AI tự động soạn nhận xét học tập để phụ huynh gửi cho con hoặc chia sẻ với giáo viên.")

    if not ai_user_names:
        st.warning("Chưa có dữ liệu học sinh.")
    else:
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            report_target = st.selectbox(
                "Chọn học sinh:",
                ai_user_names,
                key="ai_report_select"
            )
        with r_col2:
            report_type = st.selectbox(
                "Loại nhận xét:",
                [
                    "📩 Nhắn nhủ động viên gửi cho con",
                    "📋 Báo cáo tuần gửi giáo viên",
                    "👨‍👩‍👧 Tóm tắt chia sẻ với ông bà",
                    "🏆 Lời khen thưởng khi đạt mục tiêu",
                    "⚠️ Nhắc nhở nhẹ nhàng khi chưa đạt"
                ],
                key="ai_report_type"
            )

        extra_note = st.text_input(
            "Ghi chú thêm cho AI (không bắt buộc):",
            placeholder="Ví dụ: Con đang chuẩn bị thi học kỳ, cần tập trung Toán...",
            key="ai_extra_note"
        )

        gen_report = st.button("✍️ Tạo nhận xét", type="secondary",
                               use_container_width=True, key="btn_gen_report")

        if gen_report and report_target:
            u_info  = res_ai.get(report_target, {})
            summary = build_student_summary(report_target, u_info)

            type_prompts = {
                "📩 Nhắn nhủ động viên gửi cho con": (
                    f"Viết một tin nhắn ngắn (5-7 câu) từ phụ huynh gửi cho con tên {report_target}, "
                    f"dựa trên dữ liệu học tập này:\n{summary}\n"
                    f"Giọng ấm áp, thương yêu, khích lệ con tiếp tục cố gắng. "
                    f"{'Ghi chú thêm: ' + extra_note if extra_note else ''}"
                ),
                "📋 Báo cáo tuần gửi giáo viên": (
                    f"Soạn báo cáo học tập tuần này của học sinh {report_target} để phụ huynh gửi giáo viên. "
                    f"Dữ liệu:\n{summary}\n"
                    f"Viết chuyên nghiệp, trình bày rõ ràng theo cấu trúc: "
                    f"Tổng quan / Môn học / Thời gian / Nhận xét / Kiến nghị. "
                    f"{'Ghi chú: ' + extra_note if extra_note else ''}"
                ),
                "👨‍👩‍👧 Tóm tắt chia sẻ với ông bà": (
                    f"Viết đoạn tóm tắt ngắn (3-5 câu) về tình hình học tập của {report_target} "
                    f"để phụ huynh chia sẻ với ông bà. Giọng vui vẻ, tự hào, dễ hiểu. "
                    f"Dữ liệu:\n{summary}\n"
                    f"{'Ghi chú: ' + extra_note if extra_note else ''}"
                ),
                "🏆 Lời khen thưởng khi đạt mục tiêu": (
                    f"Viết lời khen ngợi (4-6 câu) dành cho {report_target} vì đã đạt mục tiêu học tập. "
                    f"Dữ liệu:\n{summary}\n"
                    f"Giọng hào hứng, tự hào, có thể đề xuất phần thưởng phù hợp. "
                    f"{'Ghi chú: ' + extra_note if extra_note else ''}"
                ),
                "⚠️ Nhắc nhở nhẹ nhàng khi chưa đạt": (
                    f"Viết lời nhắc nhở nhẹ nhàng (4-6 câu) cho {report_target} khi chưa đạt mục tiêu. "
                    f"Dữ liệu:\n{summary}\n"
                    f"Giọng quan tâm, không la mắng, giúp con hiểu cần cố gắng hơn. "
                    f"{'Ghi chú: ' + extra_note if extra_note else ''}"
                ),
            }

            prompt = type_prompts.get(report_type, "")

            with st.spinner("✍️ Gemini đang soạn nội dung..."):
                report_result = call_gemini(prompt)

            st.markdown("---")
            st.markdown(f"**📄 Nội dung được tạo — {report_type}**")
            with st.container(border=True):
                st.markdown(report_result)

            c_copy, c_send = st.columns(2)
            with c_copy:
                st.download_button(
                    "📥 Tải về file .txt",
                    data=report_result,
                    file_name=f"nhan_xet_{report_target}_{datetime.date.today()}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    type="secondary",
                    key="dl_report"
                )
            with c_send:
                if st.button("📤 Gửi vào phòng chat luôn", use_container_width=True,
                             type="secondary", key="send_report_chat"):
                    try:
                        now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
                        requests.post(
                            f"{base_url}chats.json",
                            json={
                                "sender": f"🤖 AI PHUY HUYNH ({st.session_state.get('username')})",
                                "text": report_result,
                                "time": now_vn.strftime("%H:%M")
                            },
                            timeout=2
                        )
                        st.success("✅ Đã gửi vào phòng chat!")
                    except:
                        st.error("Lỗi gửi chat.")

            if st.button("💾 Lưu nhận xét vào hồ sơ học sinh", key="save_report",
                         use_container_width=True):
                try:
                    now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
                    requests.patch(
                        f"{base_url}users/{report_target}.json",
                        json={
                            "last_report": report_result,
                            "last_report_type": report_type,
                            "last_report_time": now_vn.strftime("%d/%m/%Y %H:%M")
                        },
                        timeout=3
                    )
                    st.success("✅ Đã lưu vào hồ sơ!")
                except:
                    st.error("Lỗi lưu Firebase.")
# =====================================================================
# 💬 PHÒNG CHAT
# =====================================================================
st.write("---")
st.subheader("💬 Nhật ký tin nhắn công cộng")

# ── Hiển thị tin nhắn ──
chats = {}
try:
    res = requests.get(f"{base_url}chats.json", timeout=2).json()
    if res and isinstance(res, dict): chats = res
except Exception: pass

if chats:
    for cid, m in list(chats.items())[-8:]:
        if not isinstance(m, dict): continue
        sender = m.get("sender", "Ẩn danh")
        text   = m.get("text", "")
        ts     = m.get("time", "--:--")
        is_parent = "PHỤ HUYNH" in sender.upper() or "AI" in sender.upper()
        
        border_color = "#a78bfa" if is_parent else "#38bdf8"
        avatar = "👑" if "PHỤ HUYNH" in sender.upper() else "🤖" if "AI" in sender.upper() else "👤"
        
        with st.container(border=True):
            if m.get("type") == "revoked":
                st.markdown(
                    f'<div style="color:#475569;font-style:italic;font-size:0.83rem;padding:4px 0;">'
                    f'🚫 <em>{sender} đã thu hồi một tin nhắn.</em></div>',
                    unsafe_allow_html=True
                )
            else:
                is_reaction = len(text.strip()) <= 4 and not text.strip().isascii()
                if is_reaction:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0;">'
                        f'<span style="font-size:2rem;">{text}</span>'
                        f'<span style="color:#475569;font-size:0.78rem;">{avatar} {sender} · {ts}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div style="background:{"rgba(167,139,250,0.07)" if is_parent else "rgba(56,189,248,0.07)"}; '
                        f'border-left:3px solid {border_color};border-radius:0 12px 12px 0;'
                        f'padding:10px 14px;margin-bottom:2px;">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">'
                        f'<span style="color:{border_color};font-weight:600;font-size:0.82rem;">{avatar} {sender}</span>'
                        f'<span style="color:#475569;font-size:0.74rem;">🕒 {ts}</span>'
                        f'</div>'
                        f'<div style="color:#e2e8f0;font-size:0.92rem;line-height:1.5;">{text}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                
                col_r1, col_r2, col_r3 = st.columns([1, 1, 4])
                with col_r1:
                    if st.button("✂️ Gỡ", key=f"del_{cid}", type="primary", use_container_width=True):
                        try:
                            requests.patch(f"{base_url}chats/{cid}.json", json={"text": "", "type": "revoked"}, timeout=2)
                        except: pass
                        st.rerun()
                with col_r2:
                    if st.button("❤️", key=f"react_{cid}", use_container_width=True):
                        try:
                            now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
                            requests.post(f"{base_url}chats.json", json={
                                "sender": f"PHỤ HUYNH ({st.session_state.get('username', 'Phụ huynh')}) 👑",
                                "text": "❤️",
                                "time": now_vn.strftime("%H:%M"),
                                "type": "reaction"
                            }, timeout=2)
                        except: pass
                        st.rerun()
else:
    st.markdown(
        '<div style="text-align:center;padding:2rem;color:#475569;">'
        '<div style="font-size:2.5rem;margin-bottom:0.5rem;">💬</div>'
        '<div style="font-size:0.9rem;">Chưa có tin nhắn nào. Hãy gửi lời nhắn đầu tiên!</div>'
        '</div>',
        unsafe_allow_html=True
    )

# ── Emoji quick-pick ──
st.markdown("<div style='margin:8px 0 4px;font-size:0.8rem;color:#475569;'>Gửi nhanh emoji:</div>", unsafe_allow_html=True)
emoji_cols = st.columns(8)
quick_emojis = ["👍", "❤️", "🔥", "🎉", "💪", "😊", "👏", "⭐"]

for i, em in enumerate(quick_emojis):
    with emoji_cols[i]:
        if st.button(em, key=f"qemoji_{em}", use_container_width=True):
            try:
                now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
                requests.post(f"{base_url}chats.json", json={
                    "sender": f"PHỤ HUYNH ({st.session_state.get('username', 'Phụ huynh')}) 👑",
                    "text": em,
                    "time": now_vn.strftime("%H:%M"),
                    "type": "reaction"
                }, timeout=2)
            except: pass
            st.rerun()

# ── Ô nhập tin nhắn ──
st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

if "temp_text" not in st.session_state:
    st.session_state["temp_text"] = ""

msg_input = st.text_input(
    "Nhập tin nhắn:",
    value=st.session_state["temp_text"],
    key="chat_input_box",
    placeholder="💬 Gõ nội dung rồi bấm Gửi...",
    label_visibility="collapsed"
)

send_col, clear_col = st.columns([4, 1])
with send_col:
    if st.button("📤 Gửi tin nhắn", use_container_width=True, key="btn_send_chat"):
        text_to_send = msg_input.strip()
        if text_to_send:
            now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
            try:
                requests.post(
                    f"{base_url}chats.json",
                    json={
                        "sender": f"PHỤ HUYNH ({st.session_state.get('username', 'Phụ huynh')}) 👑",
                        "text":   text_to_send,
                        "time":   now_vn.strftime("%H:%M")
                    },
                    timeout=2
                )
                st.session_state["temp_text"] = ""
            except Exception:
                st.warning("⚠️ Mất kết nối, tin nhắn chưa gửi được.")
            st.session_state["chat_counter"] = st.session_state.get("chat_counter", 0) + 1
            st.rerun()

with clear_col:
    if st.button("🗑️ Xóa", use_container_width=True, key="btn_clear_chat"):
        st.session_state["temp_text"] = ""
        st.session_state["chat_counter"] = st.session_state.get("chat_counter", 0) + 1
        st.rerun()
