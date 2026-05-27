import streamlit as st
import requests
import time
import socket
import qrcode
import pandas as pd
from io import BytesIO
import datetime  
import hashlib

# ── 🔴 URL FIREBASE GỐC CHUẨN ĐANG DÙNG CHUNG ──
FIREBASE_URL = "https://pomodoroapp-701a2-default-rtdb.firebaseio.com/"

st.set_page_config(
    page_title="Trung Tâm Điều Khiển Phụ Huynh", 
    page_icon="👑", 
    layout="wide", # Nâng cấp sang chế độ màn hình rộng để chia cột chuyên nghiệp
    initial_sidebar_state="expanded"
)

# =====================================================================
# 🎨 SIÊU NÂNG CẤP GIAO DIỆN PREMIUM (SCROLLBAR, ANIMATION & CARD 3D)
# =====================================================================
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

if st.session_state["theme_mode"] == "🌙 Giao diện Tối":
    st.markdown("""
        <style>
        /* 1. THANH CUỘT TÙY CHỈNH (CYBERPUNK SCROLLBAR) */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #38bdf8; }

        /* Nền ứng dụng tối */
        .stApp { background-color: #0f172a; color: #f1f5f9; transition: background-color 0.3s ease; }
        [data-testid="stHeader"] { background-color: rgba(15, 23, 42, 0.8); backdrop-filter: blur(8px); }
        
        /* 2. HIỆU ỨNG CARD 3D KHI RE CHUỘT */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #1e293b !important; 
            border: 1px solid #334155 !important;
            border-radius: 14px !important; 
            padding: 22px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px); 
            border-color: #38bdf8 !important; 
            box-shadow: 0 15px 25px -5px rgba(56, 189, 248, 0.15) !important; 
        }
        
        /* Màu tiêu đề Cyberpunk Gradient */
        h1, h2, h3 { 
            background: linear-gradient(to right, #38bdf8, #818cf8) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 700 !important;
        }
        
        section[data-testid="stSidebar"] { background-color: #0b0f19 !important; border-right: 1px solid #1e293b; }
        
        /* Ô nhập liệu và Ép chữ Selectbox */
        .stTextInput input, .stNumberInput input, div[data-baseweb="select"] {
            background-color: #0f172a !important; 
            color: #f1f5f9 !important; 
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] * { color: #f1f5f9 !important; }
        
        /* 3. HIỆU ỨNG PHÁT SÁNG CHẬM (PULSE ANIMATION) CHO NÚT CHÍNH */
        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #ef4444, #b91c1c) !important; 
            border: none !important; color: white !important; font-weight: bold !important;
            border-radius: 8px !important; transition: all 0.25s ease-in-out !important;
            animation: pulse-red 2s infinite;
        }
        button[data-testid="baseButton-primary"]:hover { 
            transform: scale(1.02); 
            animation: none; 
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.7) !important; 
        }
        
        /* Nút Bấm Secondary */
        button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #38bdf8, #2563eb) !important; 
            color: white !important; font-weight: bold !important; border: none !important;
            border-radius: 8px !important; transition: all 0.25s ease-in-out !important;
        }
        button[data-testid="baseButton-secondary"]:hover { 
            transform: translateY(-1px);
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.6) !important; 
        }
        
        /* Khung chat tinh gọn */
        .chat-box { background-color: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #38bdf8; }
        .badge-custom { background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        /* 1. THANH CUỘT BẢN SÁNG (MINIMALIST SCROLLBAR) */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #f8fafc; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

        /* Nền ứng dụng sáng */
        .stApp { background-color: #f8fafc; color: #0f172a; transition: background-color 0.3s ease; }
        [data-testid="stHeader"] { background-color: rgba(248, 250, 252, 0.8); backdrop-filter: blur(8px); }
        
        /* 2. HIỆU ỨNG CARD CHO BẢN SÁNG */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important; 
            border: 1px solid #e2e8f0 !important;
            border-radius: 14px !important; 
            padding: 22px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
            transition: transform 0.25s ease, box-shadow 0.25s ease !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.08) !important;
        }
        
        h1, h2, h3 { 
            color: #0284c7 !important; 
            background: none !important;
            -webkit-text-fill-color: initial !important; 
            font-weight: 700 !important; 
        }
        
        section[data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
        
        .stTextInput input, .stNumberInput input, div[data-baseweb="select"] {
            background-color: #ffffff !important; 
            color: #0f172a !important; 
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] * { color: #0f172a !important; }
        
        /* Nút Bấm Primary bản sáng */
        button[data-testid="baseButton-primary"] {
            background-color: #dc2626 !important; 
            border: none !important; color: white !important; font-weight: bold !important;
            border-radius: 8px !important; transition: all 0.25s ease-in-out !important;
        }
        button[data-testid="baseButton-primary"]:hover { background-color: #b91c1c !important; transform: translateY(-1px); }
        
        /* Nút Bấm Secondary bản sáng */
        button[data-testid="baseButton-secondary"] {
            background-color: #0284c7 !important; 
            color: white !important; font-weight: bold !important; border: none !important;
            border-radius: 8px !important; transition: all 0.25s ease-in-out !important;
        }
        button[data-testid="baseButton-secondary"]:hover { background-color: #0369a1 !important; transform: translateY(-1px); }
        
        .chat-box { background-color: #f1f5f9; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #0284c7; }
        .badge-custom { background-color: #dc2626; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
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
# 🔒 LỚP BẢO MẬT: MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ
# =====================================================================
if not st.session_state["authenticated"] and st.session_state["auth_page"] == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h2 style='text-align: center;'>🔑 ĐĂNG NHẬP PHỤ HUYNH</h2>", unsafe_allow_html=True)
        username_input = st.text_input("Tên đăng nhập:", key="login_user", placeholder="Nhập tài khoản...")
        password_input = st.text_input("Mật khẩu:", type="password", key="login_pass", placeholder="Nhập mật khẩu...")
        
        if st.button("Đăng nhập hệ thống 🚀", use_container_width=True, type="primary"):
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
                    else:
                        st.error("❌ Sai tài khoản hoặc mật khẩu!")
                except Exception:
                    st.error("❌ Không thể kết nối tới Firebase! Kiểm tra mạng hoặc URL.")
            else:
                st.warning("Vui lòng nhập đủ tài khoản và mật khẩu!")
                
        st.write("---")
        st.caption("Chưa có tài khoản quản lý?")
        if st.button("Tạo tài khoản mới (Đăng ký) ✨", use_container_width=True):
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
        
        if st.button("Hoàn tất Đăng ký 🛠️", use_container_width=True, type="primary"):
            u = reg_user.strip()
            p = reg_pass.strip()
            if u and p:
                if p != reg_confirm.strip():
                    st.error("❌ Mật khẩu xác nhận không khớp!")
                else:
                    try:
                        check_res = requests.get(f"{base_url}accounts/{u}.json", timeout=3)
                        if check_res.json() is not None:
                            st.error("❌ Tên đăng nhập này đã tồn tại!")
                        else:
                            requests.put(f"{base_url}accounts/{u}.json", json={"password": hash_password(p)}, timeout=3)
                            st.success("🎉 Đăng ký thành công! Đang chuyển về trang Đăng nhập...")
                            st.session_state["auth_page"] = "login"
                            time.sleep(1.5)
                            st.rerun()
                    except Exception:
                        st.error("❌ Lỗi kết nối gửi dữ liệu lên Firebase!")
            else:
                st.warning("Vui lòng điền đầy đủ thông tin ô trống!")
                
        st.write("---")
        if st.button("Quay lại Đăng nhập ↩️", use_container_width=True):
            st.session_state["auth_page"] = "login"
            st.rerun()
    st.stop()

# =====================================================================
# 🎛️ LOGIC CHỨC NĂNG HỆ THỐNG GIAO DIỆN CHÍNH
# =====================================================================
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "local_chats" not in st.session_state:
    st.session_state.local_chats = {}

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

def send_parent_msg():
    msg_text = st.session_state.widget_msg.strip()
    if msg_text:
        now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
        current_time = now_vn.strftime("%H:%M")
        new_msg = {
            "sender": f"PHỤ HUYNH ({st.session_state.get('username')}) 👤", 
            "text": msg_text, 
            "time": current_time
        }
        try:
            requests.post(f"{base_url}chats.json", json=new_msg, timeout=2)
            st.toast("Đã gửi lời nhắc lên hệ thống!", icon="🚀")
        except Exception:
            st.toast("Chế độ Local: Đã lưu tạm tin nhắn!", icon="💻")
        st.session_state.widget_msg = ""

def revoke_msg(chat_id):
    if chat_id.startswith("local_"):
        if chat_id in st.session_state.local_chats:
            st.session_state.local_chats[chat_id]["text"] = "đã bị phụ huynh gỡ bỏ."
            st.session_state.local_chats[chat_id]["type"] = "revoked"
            st.toast("Đã gỡ tin nhắn tạm!", icon="✂️")
    else:
        try:
            requests.patch(f"{base_url}chats/{chat_id}.json", json={"text": "đã bị phụ huynh gỡ bỏ.", "type": "revoked"}, timeout=2)
            st.toast("Đã gỡ tin nhắn trên đám mây!", icon="✂️")
        except Exception: 
            st.toast("Lỗi kết nối mạng!", icon="❌")

def send_remote_command(payload, target_user):
    try:
        requests.put(f"{base_url}commands/{target_user}.json", json=payload, timeout=2)
        st.toast(f"🚨 Đã chuyển lệnh thành công tới {target_user}!", icon="⚡")
    except Exception: 
        st.error("Lỗi kết nối mạng Firebase.")

def clear_all_chats():
    try:
        res = requests.delete(f"{base_url}chats.json", timeout=2)
        if res.status_code == 200:
            st.session_state.local_chats = {}
            st.toast("🧹 Đã làm sạch phòng chat lỗi!", icon="🧼")
    except Exception: 
        pass

# --- TIÊU ĐỀ HỆ THỐNG ---
st.markdown("<h1 style='margin-bottom:0px;'>👑 Trung Tâm Quản Lý Phụ Huynh Tối Thượng</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748b; font-size:14px; margin-top:-5px;'>Hệ thống giám sát tối cao, điều khiển từ xa và lá chắn an toàn cho máy con</p>", unsafe_allow_html=True)

with st.sidebar:
    st.write(f"### 👤 Tài khoản: `{st.session_state.get('username')}`")
    if st.button("🔒 Đăng xuất ứng dụng", use_container_width=True, type="primary"):
        st.session_state["authenticated"] = False
        st.rerun()

# --- HÀNG THÔNG SỐ METRICS VIP ---
status_db = "Kết nối tốt 🟢"
try:
    res_test = requests.get(f"{base_url}chats.json", timeout=1.5)
    if res_test.status_code != 200: status_db = "Lỗi kết nối 🔴"
except Exception: 
    status_db = "Ngoại tuyến 🟡"

m1, m2, m3 = st.columns(3)
with m1: st.metric(label="📡 Máy chủ Firebase", value=status_db)
with m2:
    @st.fragment(run_every=1)
    def live_clock():
        now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
        st.metric(label="⏱️ Đồng hồ hệ thống", value=now_vn.strftime("%H:%M:%S"))
    live_clock()
with m3: st.metric(label="💬 Tin nhắc tạm", value=f"{len(st.session_state.local_chats)} tin")

st.write("---")

# Quét tìm danh sách máy con trước để phục vụ hiển thị
user_names = []
user_times = []
try:
    res_users = requests.get(f"{base_url}users.json", timeout=3)
    if res_users.status_code == 200 and res_users.json():
        users_data = res_users.json()
        for u_id, u_info in users_data.items():
            if isinstance(u_info, dict):
                user_names.append(u_id)
                user_times.append(u_info.get("study_seconds", 0) // 60)
except Exception:
    pass

# =====================================================================
# 🗂️ CHIA LAYOUT 2 CỘT CHUYÊN NGHIỆP (DASHBOARD GRID)
# =====================================================================
col_left, col_right = st.columns([1.1, 0.9], gap="large")

# 🏛️ CỘT TRÁI: GIÁM SÁT HỌC TẬP & TRUNG TÂM ĐIỀU KHIỂN TỪ XA
with col_left:
    with st.container(border=True):
        st.markdown("### 📊 Phân Tích & Giám Sát Học Tập")
        
        @st.fragment(run_every=5)
        def render_online_status():
            try:
                res_live = requests.get(f"{base_url}users.json", timeout=2)
                if res_live.status_code == 200 and res_live.json():
                    live_data = res_live.json()
                    for u_id, u_info in live_data.items():
                        if isinstance(u_info, dict):
                            badge = "<span style='color:#10b981;font-weight:bold;'>● Trực tuyến</span>" if u_info.get("status") == "online" else "<span style='color:#64748b;'>⚫ Ngoại tuyến</span>"
                            st.markdown(f"💻 Máy: **{u_id}** &nbsp;|&nbsp; {badge} &nbsp;|&nbsp; ⏱️ Đã học: `{u_info.get('study_seconds', 0) // 60} phút`", unsafe_allow_html=True)
                else: st.info("Chưa có dữ liệu học sinh.")
            except Exception: st.caption("⚠️ Đang kết nối lại luồng dữ liệu...")
        render_online_status()

        if user_names:
            df = pd.DataFrame({"Học sinh": user_names, "Thời gian học (Phút)": user_times})
            st.bar_chart(data=df, x="Học sinh", y="Thời gian học (Phút)", color="#38bdf8")
        else:
            st.info("Biểu đồ trống: Đang chờ máy con kết nối...")

    st.write("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### ⚡ Điều Khiển & Giao Mục Tiêu Từ Xa")
        if user_names:
            target = st.selectbox("🎯 Chọn con để điều khiển:", user_names, key="target_select")
            
            c_cmd1, c_cmd2 = st.columns(2)
            with c_cmd1:
                if st.button("🔔 PHÁT CHUÔNG CHÚ Ý", use_container_width=True, key="btn_buzz"):
                    send_remote_command({"command": "ALERT_BUZZ", "timestamp": int(time.time()), "status": "pending"}, target)
                target_mins = st.number_input("Đặt mục tiêu học hôm nay (Phút):", min_value=5, max_value=180, value=30, step=5, key="num_goal")
                if st.button("🚀 Gửi Mục Tiêu Thời Gian", use_container_width=True, key="btn_set_goal", type="secondary"):
                    send_remote_command({"command": "SET_GOAL", "minutes": target_mins, "timestamp": int(time.time()), "status": "pending"}, target)
            with c_cmd2:
                if st.button("🛑 LỆNH NGHỈ NGƠI (KHÓA APP)", type="primary", use_container_width=True, key="btn_break"):
                    send_remote_command({"command": "FORCE_BREAK", "timestamp": int(time.time()), "status": "pending"}, target)
                sticky_msg = st.text_input("Lời nhắn ghim màn hình app con:", placeholder="Ví dụ: Tập trung con nhé...", key="txt_sticky")
                if st.button("📌 Ghim Lời Nhắc Lên Màn Hình", use_container_width=True, key="btn_sticky"):
                    if sticky_msg.strip():
                        send_remote_command({"command": "SET_STICKY", "text": sticky_msg.strip()}, target)
                        try:
                            requests.put(f"{base_url}sticky/{target}.json", json={"text": sticky_msg.strip()}, timeout=2)
                            st.toast("📌 Đã ghim lời nhắc thành công!", icon="💛")
                        except: pass
        else: 
            st.info("Không có học sinh trực tuyến để điều khiển.")

# 🛡️ CỘT PHẢI: LÁ CHẮN AN TOÀN (ANTI-PROC), KHUNG CHAT ĐỒNG BỘ & QR CODE
with col_right:
    with st.container(border=True):
        st.markdown("### 🛡️ Safety Search Guard (Giám sát & Chặn Từ Cấm)")
        current_blacklist = []
        try:
            res_bl = requests.get(f"{base_url}blacklist_keywords.json", timeout=2)
            if res_bl.json(): current_blacklist = res_bl.json()
        except: pass
        
        st.write(f"🚫 Từ khóa cấm: `{', '.join(current_blacklist) if current_blacklist else 'Trống'}`")
        
        col_bl1, col_bl2 = st.columns([2.2, 1])
        with col_bl1:
            new_word = st.text_input("Thêm từ khóa cấm mới:", placeholder="Ví dụ: game, phim...", key="txt_new_badword", label_visibility="collapsed")
        with col_bl2:
            if st.button("➕ Thêm Từ", use_container_width=True):
                if new_word.strip() and new_word.strip().lower() not in current_blacklist:
                    current_blacklist.append(new_word.strip().lower())
                    requests.put(f"{base_url}blacklist_keywords.json", json=current_blacklist, timeout=2)
                    st.toast("Đã cập nhật từ khóa cấm!", icon="💾")
                    st.rerun()
                    
        if st.button("🧼 Xóa sạch danh sách từ cấm", key="btn_clear_blacklist", type="primary", use_container_width=True):
            requests.delete(f"{base_url}blacklist_keywords.json", timeout=2)
            st.rerun()

        st.write("---")
        
        @st.fragment(run_every=4)
        def render_safety_logs():
            try:
                res_alerts = requests.get(f"{base_url}safety_alerts.json", timeout=2)
                if res_alerts.json():
                    for aid, info in list(res_alerts.json().items())[-2:]:
                        st.markdown(f"<div style='background-color:rgba(239,68,68,0.12); padding:10px; border-radius:6px; border-left:4px solid #ef4444; margin-bottom:8px; color:#f87171; font-size:13px;'>🚨 <b>VI PHẠM:</b> Máy con vừa gõ từ khóa cấm <b>{info.get('keyword')}</b> lúc {info.get('time')}!</div>", unsafe_allow_html=True)
            except: pass
            
            try:
                res_logs = requests.get(f"{base_url}key_logs.json", timeout=2)
                if res_logs.json():
                    st.markdown("<small style='color:#64748b;'>📋 Nhật ký gõ phím live:</small>", unsafe_allow_html=True)
                    for lid, text_line in list(res_logs.json().items())[-3:]:
                        st.caption(f"🕒 {text_line.get('time', '--:--')} → `{text_line.get('text', '')}`")
            except: pass
        render_safety_logs()

    st.write("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        # Đồng bộ danh sách Chat công cộng
        chats = {}
        try:
            res = requests.get(f"{base_url}chats.json", timeout=2)
            if res.status_code == 200 and res.json() and isinstance(res.json(), dict): chats = res.json()
        except: pass
        all_chats = {**chats, **st.session_state.local_chats}
        
        c_title, c_clr = st.columns([2, 1])
        with c_title: st.markdown(f"### 💬 Nhật Ký Tin Nhắn ({len(all_chats)})")
        with c_clr:
            if st.button("🧼 Dọn chat", type="secondary", key="btn_clear_chat", use_container_width=True):
                clear_all_chats()
                st.rerun()

        # Hiển thị Chat Box cuộn mượt bằng CSS card
        if not all_chats: st.info("Chưa có tin nhắn nào trong phòng.")
        else:
            for cid, m in list(all_chats.items())[-6:]:
                if not isinstance(m, dict): continue
                sender = m.get("sender", "Ẩn danh")
                text = m.get("text", "")
                ts = m.get("time", "--:--")
                
                if m.get("type") == "revoked":
                    st.markdown(f"<div style='color:#64748b; font-size:13px; font-style:italic; padding:4px;'>⚠️ {sender} {text}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-box">
                        <small style="color:#38bdf8; font-weight:bold;">{sender}</small>
                        <small style="color:#64748b; float:right;">🕒 {ts}</small>
                        <p style="margin:4px 0 0 0; font-size:14px;">{text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("✂️ Gỡ tin", key=f"del_{cid}", use_container_width=True):
                        revoke_msg(cid)
                        st.rerun()

        st.text_input("Gửi tin nhắn nhanh xuống máy con:", key="widget_msg", placeholder="Nhập lời nhắc...", on_change=send_parent_msg)
        st.button("Gửi tin nhắn ➤", key="btn_send_msg", on_click=send_parent_msg, use_container_width=True, type="secondary")

# --- BOTTOM BAR: QR CODE KẾT NỐI NHANH ---
st.write("<br>", unsafe_allow_html=True)
qr_bytes, net_url = generate_network_qr()
if qr_bytes and net_url:
    with st.expander("📲 MÃ QR KẾT NỐI ĐIỆN THOẠI DI ĐỘNG", expanded=False):
        col_qr, col_btn = st.columns([1, 4])
        with col_qr: st.image(qr_bytes, width=130)
        with col_btn:
            st.markdown(f"⚙️ **Quét mã để điều khiển bằng điện thoại:**")
            st.caption(f"Đường dẫn máy chủ: `{net_url}`")
            st.download_button(label="📥 Tải ảnh QR Code", data=qr_bytes, file_name="Ma_QR_Parent.png", mime="image/png", key="download_qr_btn")
