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
    layout="centered", # Bản dọc tập trung tối ưu trải nghiệm mobile/desktop
    initial_sidebar_state="expanded"
)

# =====================================================================
# 🎨 GIAO DIỆN PREMIUM (MƯỢT MÀ, ĐÃ ĐƯỢC ĐỒNG BỘ CSS)
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
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #38bdf8; }
        .stApp { background-color: #0f172a; color: #f1f5f9; transition: background-color 0.3s ease; }
        [data-testid="stHeader"] { background-color: rgba(15, 23, 42, 0.8); backdrop-filter: blur(8px); }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #1e293b !important; 
            border: 1px solid #334155 !important;
            border-radius: 14px !important; 
            padding: 22px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px); border-color: #38bdf8 !important; 
            box-shadow: 0 15px 25px -5px rgba(56, 189, 248, 0.15) !important; 
        }
        h1, h2, h3 { 
            background: linear-gradient(to right, #38bdf8, #818cf8) !important;
            -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; font-weight: 700 !important;
        }
        section[data-testid="stSidebar"] { background-color: #0b0f19 !important; border-right: 1px solid #1e293b; }
        .stTextInput input, .stNumberInput input, div[data-baseweb="select"] {
            background-color: #0f172a !important; color: #f1f5f9 !important; border: 1px solid #475569 !important; border-radius: 8px !important;
        }
        div[data-baseweb="select"] * { color: #f1f5f9 !important; }
        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #ef4444, #b91c1c) !important; border: none !important; color: white !important; font-weight: bold !important;
            border-radius: 8px !important; transition: all 0.25s ease-in-out !important; animation: pulse-red 2s infinite;
        }
        button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #38bdf8, #2563eb) !important; color: white !important; font-weight: bold !important; border: none !important;
            border-radius: 8px !important; transition: all 0.25s ease-in-out !important;
        }
        button[data-testid="baseButton-secondary"]:hover { transform: translateY(-1px); box-shadow: 0 0 15px rgba(56, 189, 248, 0.6) !important; }
        .chat-box { background-color: #1e293b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #38bdf8; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #f8fafc; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
        .stApp { background-color: #f8fafc; color: #0f172a; transition: background-color 0.3s ease; }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 14px !important; padding: 22px !important; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        }
        h1, h2, h3 { color: #0284c7 !important; background: none !important; -webkit-text-fill-color: initial !important; font-weight: 700 !important; }
        section[data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
        .stTextInput input, .stNumberInput input, div[data-baseweb="select"] { background-color: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; }
        button[data-testid="baseButton-primary"] { background-color: #dc2626 !important; border: none !important; color: white !important; font-weight: bold !important; border-radius: 8px !important; }
        button[data-testid="baseButton-secondary"] { background-color: #0284c7 !important; color: white !important; font-weight: bold !important; border: none !important; border-radius: 8px !important; }
        .chat-box { background-color: #f1f5f9; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #0284c7; }
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
# 🔒 LỚP BẢO MẬT ĐĂNG NHẬP
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
                    else: st.error("❌ Sai tài khoản hoặc mật khẩu!")
                except Exception: st.error("❌ Lỗi kết nối tới Firebase!")
        st.write("---")
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
# KHỞI TẠO BIẾN TRẠNG THÁI CƠ SỞ
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

def send_parent_msg():
    msg_text = st.session_state.widget_msg.strip()
    if msg_text:
        now_vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
        new_msg = {"sender": f"PHỤ HUYNH ({st.session_state.get('username')}) 👤", "text": msg_text, "time": now_vn.strftime("%H:%M")}
        try: requests.post(f"{base_url}chats.json", json=new_msg, timeout=2)
        except Exception: pass
        st.session_state.widget_msg = ""

def revoke_msg(chat_id):
    try: requests.patch(f"{base_url}chats/{chat_id}.json", json={"text": "đã bị phụ huynh gỡ bỏ.", "type": "revoked"}, timeout=2)
    except Exception: pass

def send_remote_command(payload, target_user):
    try: requests.put(f"{base_url}commands/{target_user}.json", json=payload, timeout=2)
    except Exception: pass

st.title("👑 Trung Tâm Quản Lý Phụ Huynh Tối Thượng")

with st.sidebar:
    st.write(f"### 👤 Tài khoản: `{st.session_state.get('username')}`")
    if st.button("🔒 Đăng xuất ứng dụng", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

# ⏱️ Đồng hồ và Trạng thái Server
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
# 🏆 TÍNH NĂNG: BẢNG XẾP HẠNG THI ĐUA CHĂM CHỈ
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
            
            st.dataframe(df_lb, use_container_width=True, hide_index=True)
            if df_lb.iloc[0]["Thời gian học (Phút)"] > 0:
                st.success(f"🎉 Tuyên dương **{df_lb.iloc[0]['Học sinh']}** đang dẫn đầu bảng xếp hạng hôm nay!")
except Exception: pass

if user_names:
    df_chart = pd.DataFrame({"Học sinh": user_names, "Thời gian học (Phút)": user_times})
    st.bar_chart(data=df_chart, x="Học sinh", y="Thời gian học (Phút)", color="#38bdf8")

# =====================================================================
# 🛡️ SAFETY SEARCH GUARD (Giám sát phím & Chặn từ cấm cũ)
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
    if st.button("➕ Thêm Từ Cấm", use_container_width=True):
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
# ⚡ TRUNG TÂM ĐIỀU KHIỂN TỪ XA
# =====================================================================
st.write("---")
st.subheader("⚡ Điều Khiển & Giao Mục Tiêu Từ Xa")
if user_names:
    target = st.selectbox("Chọn con để điều khiển:", user_names, key="target_select")
    c_cmd1, c_cmd2 = st.columns(2)
    with c_cmd1:
        if st.button("🔔 PHÁT CHUÔNG CHÚ Ý", use_container_width=True):
            send_remote_command({"command": "ALERT_BUZZ", "timestamp": int(time.time()), "status": "pending"}, target)
    with c_cmd2:
        if st.button("🛑 LỆNH NGHỈ NGƠI (KHÓA APP)", type="primary", use_container_width=True):
            send_remote_command({"command": "FORCE_BREAK", "timestamp": int(time.time()), "status": "pending"}, target)
            
    st.write("")
    c_target1, c_target2 = st.columns(2)
    with c_target1:
        target_mins = st.number_input("Đặt mục tiêu học hôm nay (Phút):", min_value=5, max_value=180, value=30, step=5)
        if st.button("🚀 Gửi Mục Tiêu Thời Gian", use_container_width=True):
            send_remote_command({"command": "SET_GOAL", "minutes": target_mins, "timestamp": int(time.time()), "status": "pending"}, target)
    with c_target2:
        sticky_msg = st.text_input("Lời nhắn ghim màn hình app con:", placeholder="Nhập tin nhắn nhắn nhủ...")
        if st.button("📌 Ghim Lời Nhắc", use_container_width=True):
            if sticky_msg.strip():
                requests.put(f"{base_url}sticky/{target}.json", json={"text": sticky_msg.strip()}, timeout=2)

st.write("---")

# QR Code
qr_bytes, net_url = generate_network_qr()
if qr_bytes:
    with st.expander("📲 MÃ QR KẾT NỐI ĐIỆN THOẠI"):
        st.image(qr_bytes, width=150)
        st.caption(f"🔗 Link: `{net_url}`")

# Phòng chat công cộng
st.write("---")
st.subheader("💬 Nhật ký tin nhắn công cộng")
chats = {}
try:
    res = requests.get(f"{base_url}chats.json", timeout=2).json()
    if res and isinstance(res, dict): chats = res
except Exception: pass

all_chats = {**chats, **st.session_state.local_chats}
if all_chats:
    for cid, m in list(all_chats.items())[-8:]:
        if not isinstance(m, dict): continue
        sender, text, ts = m.get("sender", "Ẩn danh"), m.get("text", ""), m.get("time", "--:--")
        with st.container(border=True):
            if m.get("type") == "revoked": st.markdown(f"⚠️ *{sender} {text}*")
            else:
                st.markdown(f'<div class="chat-box"><small style="color:#38bdf8; font-weight:bold;">{sender}</small><small style="color:#64748b; float:right;">🕒 {ts}</small><p style="margin:4px 0 6px 0; font-size:14px;">{text}</p></div>', unsafe_allow_html=True)
                if st.button("✂️ Gỡ tin nhắn", key=f"del_{cid}", type="primary", use_container_width=True):
                    revoke_msg(cid)
                    st.rerun()

st.text_input("Nội dung lời nhắn công cộng:", key="widget_msg", placeholder="Nhập tin nhắn...", on_change=send_parent_msg)
st.button("Gửi tin nhắn ➤", key="btn_send_msg", on_click=send_parent_msg, use_container_width=True, type="secondary")
