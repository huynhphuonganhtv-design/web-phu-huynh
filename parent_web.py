import streamlit as st
import requests
import time
import socket
import qrcode
import pandas as pd
from io import BytesIO
from datetime import datetime
import hashlib
# ── 🔴 URL FIREBASE GỐC CHUẨN ĐANG DÙNG CHUNG ──
FIREBASE_URL = "https://pomodoroapp-701a2-default-rtdb.firebaseio.com/"

st.set_page_config(
    page_title="Trung Tâm Điều Khiển Phụ Huynh", 
    page_icon="👑", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 🎨 BỘ ĐIỀU KHIỂN GIAO DIỆN SÁNG / TỐI (THEME SWITCHER)
# =====================================================================
# Khởi tạo trạng thái giao diện mặc định là Tối (Dark)
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "🌙 Giao diện Tối"

# Thiết lập thanh bên trước để người dùng chọn Sáng/Tối
with st.sidebar:
    st.markdown("<h3 style='margin-top:0;'>🎨 Cài đặt Giao diện</h3>", unsafe_allow_html=True)
    theme_choice = st.selectbox(
        "Chọn chế độ hiển thị:",
        ["🌙 Giao diện Tối", "☀️ Giao diện Sáng"],
        key="theme_select_box"
    )
    # Cập nhật session_state khi người dùng đổi lựa chọn
    st.session_state["theme_mode"] = theme_choice

# Nhúng CSS động dựa vào lựa chọn Sáng hay Tối
if st.session_state["theme_mode"] == "🌙 Giao diện Tối":
    # --- CSS CHẾ ĐỘ TỐI (DARK MODE) ---
    st.markdown("""
        <style>
        .stApp { background-color: #0f172a; color: #f1f5f9; }
        [data-testid="stHeader"] { background-color: rgba(15, 23, 42, 0.8); }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #1e293b !important; border: 1px solid #334155 !important;
            border-radius: 12px !important; padding: 20px !important;
        }
        h1, h2, h3 { color: #38bdf8 !important; }
        section[data-testid="stSidebar"] { background-color: #0b0f19 !important; border-right: 1px solid #1e293b; }
        .stTextInput input, .stNumberInput input, .stSelectbox div {
            background-color: #0f172a !important; color: #f1f5f9 !important; border: 1px solid #475569 !important;
        }
        /* Nút màu đỏ nguy hiểm */
        button[data-testid="baseButton-primary"] {
            background-color: #ef4444 !important; border-color: #ef4444 !important; color: white !important; font-weight: bold !important;
        }
        button[data-testid="baseButton-primary"]:hover { background-color: #dc2626 !important; box-shadow: 0 0 12px #ef4444; }
        /* Nút màu xanh neon */
        button[data-testid="baseButton-secondary"] {
            background-color: #38bdf8 !important; color: #0f172a !important; font-weight: bold !important; border: none !important;
        }
        button[data-testid="baseButton-secondary"]:hover { background-color: #7dd3fc !important; box-shadow: 0 0 12px #38bdf8; }
        /* Khung chat tối */
        .chat-box { background-color: #0f172a; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #38bdf8; }
        </style>
    """, unsafe_allow_html=True)
else:
    # --- CSS CHẾ ĐỘ SÁNG (LIGHT MODE) ---
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; color: #0f172a; }
        [data-testid="stHeader"] { background-color: rgba(248, 250, 252, 0.8); }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff !important; border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important; padding: 20px !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }
        h1, h2, h3 { color: #0284c7 !important; }
        section[data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
        .stTextInput input, .stNumberInput input, .stSelectbox div {
            background-color: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important;
        }
        /* Nút màu đỏ ở chế độ sáng */
        button[data-testid="baseButton-primary"] {
            background-color: #dc2626 !important; border-color: #dc2626 !important; color: white !important; font-weight: bold !important;
        }
        button[data-testid="baseButton-primary"]:hover { background-color: #b91c1c !important; }
        /* Nút màu xanh da trời ở chế độ sáng */
        button[data-testid="baseButton-secondary"] {
            background-color: #0284c7 !important; color: white !important; font-weight: bold !important; border: none !important;
        }
        button[data-testid="baseButton-secondary"]:hover { background-color: #0369a1 !important; }
        /* Khung chat sáng */
        .chat-box { background-color: #f1f5f9; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #0284c7; }
        </style>
    """, unsafe_allow_html=True)


# Xử lý chuẩn hóa URL Firebase
base_url = FIREBASE_URL.strip()
if not base_url.endswith("/"): base_url += "/"

# Khởi tạo các biến trạng thái tài khoản nếu chưa có
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "login"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================================================================
# 🔒 LỚP BẢO MẬT: MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ
# =====================================================================

# 1. GIAO DIỆN ĐĂNG NHẬP
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
                except Exception as e:
                    st.error("❌ Không thể kết nối tới Firebase! Kiểm tra mạng hoặc URL.")
            else:
                st.warning("Vui lòng nhập đủ tài khoản và mật khẩu!")
                
        st.write("---")
        st.caption("Chưa có tài khoản quản lý?")
        if st.button("Tạo tài khoản mới (Đăng ký) ✨", use_container_width=True):
            st.session_state["auth_page"] = "register"
            st.rerun()
            
    st.stop()

# 2. GIAO DIỆN ĐĂNG KÝ
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
                    except:
                        st.error("❌ Lỗi kết nối gửi dữ liệu lên Firebase!")
            else:
                st.warning("Vui lòng điền đầy đủ thông tin ô trống!")
                
        st.write("---")
        if st.button("Quay lại Đăng nhập ↩️", use_container_width=True):
            st.session_state["auth_page"] = "login"
            st.rerun()
            
    st.stop()

# =====================================================================
# 🎛️ GIAO DIỆN CHÍNH (Chỉ kích hoạt khi ĐÃ ĐĂNG NHẬP)
# =====================================================================

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "local_chats" not in st.session_state:
    st.session_state.local_chats = {}

# --- 📲 HÀM TẠO MÃ QR TỰ ĐỘNG ---
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

# --- 💬 HÀM GỬI TIN NHẮN CHAT ---
def send_parent_msg():
    msg_text = st.session_state.widget_msg.strip()
    if msg_text:
        current_time = time.strftime("%H:%M")
        new_msg = {"sender": f"PHỤ HUYNH ({st.session_state.get('username')}) 👤", "text": msg_text, "time": current_time}
        msg_id = f"local_{int(time.time())}"
        st.session_state.local_chats[msg_id] = new_msg
        try:
            requests.post(f"{base_url}chats.json", json=new_msg, timeout=2)
            st.toast("Đã gửi lời nhắc lên hệ thống!", icon="🚀")
        except:
            st.toast("Chế độ Local: Đã lưu tạm tin nhắn!", icon="💻")
        st.session_state.input_text = ""

# --- 💬 HÀM GỠ TIN NHẮN ---
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
        except: st.toast("Lỗi kết nối mạng!", icon="❌")

# --- 🚨 HÀM PHÁT LỆNH ĐIỀU KHIỂN TỪ XA CHUẨN ĐỒNG BỘ ---
def send_remote_command(payload, target_user):
    try:
        requests.put(f"{base_url}commands/{target_user}.json", json=payload, timeout=2)
        st.toast(f"🚨 Đã chuyển lệnh thành công tới {target_user}!", icon="⚡")
    except: st.error("Lỗi kết nối mạng Firebase.")

# --- 🧹 HÀM CLEAR CHAT CỨU HỘ ---
def clear_all_chats():
    try:
        res = requests.delete(f"{base_url}chats.json", timeout=2)
        if res.status_code == 200:
            st.session_state.local_chats = {}
            st.toast("🧹 Đã làm sạch phòng chat lỗi!", icon="🧼")
    except: pass

# Giao diện chính sau đăng nhập
st.title("👑 Trung Tâm Quản Lý Phụ Huynh Tối Thượng")

with st.sidebar:
    st.write(f"### 👤 Tài khoản: `{st.session_state.get('username')}`")
    if st.button("🔒 Đăng xuất ứng dụng", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

# --- THÔNG TIN TRẠNG THÁI SERVER ---
status_db = "Kết nối tốt 🟢"
try:
    res_test = requests.get(f"{base_url}chats.json", timeout=1.5)
    if res_test.status_code != 200: status_db = "Lỗi kết nối 🔴"
except: status_db = "Ngoại tuyến 🟡"

m1, m2, m3 = st.columns(3)
with m1: st.metric(label="📡 Máy chủ Firebase", value=status_db)
with m2: st.metric(label="⏱️ Đồng hồ hệ thống", value=datetime.now().strftime("%H:%M:%S"))
with m3: st.metric(label="💬 Tin nhắc tạm", value=f"{len(st.session_state.local_chats)} tin")

st.write("---")

# 📊 ── BIỂU ĐỒ GIÁM SÁT MÁY CON ──
st.subheader("📊 Phân Tích & Giám Sát Học Tập")

user_names = []
user_times = []

# Tải dữ liệu từ Firebase trước khi vẽ đồ thị
try:
    res_users = requests.get(f"{base_url}users.json", timeout=3)
    if res_users.status_code == 200 and res_users.json():
        users_data = res_users.json()
        for u_id, u_info in users_data.items():
            if isinstance(u_info, dict):
                user_names.append(u_id)
                user_times.append(u_info.get("study_seconds", 0) // 60)
except:
    pass

# Hàm cập nhật trạng thái text Online/Offline ngầm (Đảm bảo không mờ màn hình)
@st.fragment(run_every=5)
def render_online_status():
    try:
        res_live = requests.get(f"{base_url}users.json", timeout=2)
        if res_live.status_code == 200 and res_live.json():
            live_data = res_live.json()
            st.caption("🟢 **Trạng thái trực tuyến hiện tại (Tự động quét...):**")
            for u_id, u_info in live_data.items():
                if isinstance(u_info, dict):
                    status_emoji = "🟢 Trực tuyến" if u_info.get("status") == "online" else "⚫ Ngoại tuyến"
                    st.markdown(f"- 👤 **{u_id}**: {status_emoji} | Đã học hôm nay: `{u_info.get('study_seconds', 0) // 60} phút`")
        else:
            st.info("Chưa có dữ liệu học sinh.")
    except:
        st.caption("⚠️ Đang kết nối lại luồng dữ liệu...")

# Chạy vùng quét trạng thái ngầm
render_online_status()

# Vẽ biểu đồ cột ổn định
user_names = []
user_times = []
try:
    res_users = requests.get(f"{base_url}users.json", timeout=3)
    if res_users.status_code == 200 and res_users.json():
        for u_id, u_info in res_users.json().items():
            if isinstance(u_info, dict):
                user_names.append(u_id)
                user_times.append(u_info.get("study_seconds", 0) // 60)
except: pass

if user_names:
    df = pd.DataFrame({"Học sinh": user_names, "Thời gian học (Phút)": user_times})
    st.bar_chart(data=df, x="Học sinh", y="Thời gian học (Phút)", color="#38bdf8")
else:
    st.info("Biểu đồ trống: Đang chờ máy con kết nối...")

# =====================================================================
# 🛡️ CHÈN THÊM: KHU VỰC QUẢN LÝ SAFETY SEARCH GUARD VÀO ĐÂY
# =====================================================================
st.write("---")
with st.container():
    st.markdown("### 🛡️ Safety Search Guard (Giám sát bàn phím & Từ khóa cấm)")
    
    # 1. Tải và hiển thị danh sách từ cấm hiện tại
    current_blacklist = []
    try:
        res_bl = requests.get(f"{base_url}blacklist_keywords.json", timeout=2)
        if res_bl.json(): current_blacklist = res_bl.json()
    except: pass
    
    st.write(f"Danh sách từ khóa đang cấm: `{', '.join(current_blacklist) if current_blacklist else 'Trống'}`")
    
    col_bl1, col_bl2 = st.columns([3, 1])
    with col_bl1:
        new_word = st.text_input("Thêm từ khóa cấm mới (gõ thường, không dấu):", placeholder="Ví dụ: game, lau, hack...", key="txt_new_badword")
    with col_bl2:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("➕ Thêm Từ Cấm", use_container_width=True):
            if new_word.strip() and new_word.strip().lower() not in current_blacklist:
                current_blacklist.append(new_word.strip().lower())
                requests.put(f"{base_url}blacklist_keywords.json", json=current_blacklist, timeout=2)
                st.toast("Đã cập nhật từ khóa cấm lên hệ thống!", icon="💾")
                st.rerun()
                
    if st.button("🧼 Xóa sạch danh sách từ cấm", key="btn_clear_blacklist", type="primary"):
        requests.delete(f"{base_url}blacklist_keywords.json", timeout=2)
        st.rerun()

    st.write("")
    
    # 2. Vùng hiển thị Log phím gõ và Cảnh báo vi phạm (Quét ngầm)
    @st.fragment(run_every=4)
    def render_safety_logs():
        # A. Hiển thị thông báo vi phạm màu đỏ rực
        try:
            res_alerts = requests.get(f"{base_url}safety_alerts.json", timeout=2)
            if res_alerts.json():
                st.markdown("<span style='color:#ef4444; font-weight:bold;'>⚠️ PHÁT HIỆN VI PHẠM CẤM:</span>", unsafe_allow_html=True)
                for aid, info in list(res_alerts.json().items())[-3:]:
                    # Khung thông báo đỏ bắt mắt bằng CSS có sẵn trong Streamlit
                    st.error(f"🚨 MÁY CON VI PHẠM: Vừa gõ từ khóa cấm \"{info.get('keyword')}\" lúc {info.get('time')}. Hệ thống đã cưỡng chế tắt trình duyệt!")
        except: pass
        
        # B. Hiển thị nhật ký gõ phím thông thường
        try:
            res_logs = requests.get(f"{base_url}key_logs.json", timeout=2)
            if res_logs.json():
                st.write("📋 **Nhật ký gõ phím từ máy con (Live):**")
                for lid, text_line in list(res_logs.json().items())[-5:]:
                    st.caption(f"🕒 {text_line.get('time', '--:--')} → `{text_line.get('text', '')}`")
        except: pass

    render_safety_logs()

# =====================================================================

st.write("---")

# ⚡ ── TRUNG TÂM ĐIỀU KHIỂN TỪ XA ──
st.subheader("⚡ Điều Khiển & Giao Mục Tiêu Từ Xa")
if user_names:
    target = st.selectbox("Chọn con để điều khiển:", user_names, key="target_select")
    
    c_cmd1, c_cmd2 = st.columns(2)
    with c_cmd1:
        if st.button("🔔 PHÁT CHUÔNG CHÚ Ý", use_container_width=True, key="btn_buzz"):
            payload = {"command": "ALERT_BUZZ", "timestamp": int(time.time()), "status": "pending"}
            send_remote_command(payload, target)
    with c_cmd2:
        if st.button("🛑 LỆNH NGHỈ NGƠI (KHÓA APP)", type="primary", use_container_width=True, key="btn_break"):
            payload = {"command": "FORCE_BREAK", "timestamp": int(time.time()), "status": "pending"}
            send_remote_command(payload, target)
            
    st.write("")
    c_target1, c_target2 = st.columns(2)
    with c_target1:
        target_mins = st.number_input("Đặt mục tiêu học hôm nay (Phút):", min_value=5, max_value=180, value=30, step=5, key="num_goal")
        if st.button("🚀 Gửi Mục Tiêu Thời Gian", use_container_width=True, key="btn_set_goal"):
            payload = {
                "command": "SET_GOAL", 
                "minutes": target_mins, 
                "timestamp": int(time.time()), 
                "status": "pending"
            }
            send_remote_command(payload, target)
            
    with c_target2:
        sticky_msg = st.text_input("Lời nhắn ghim màn hình app con:", placeholder="Ví dụ: Học xong nhớ làm bài tập...", key="txt_sticky")
        if st.button("📌 Ghim Lời Nhắc Lên Màn Hình", use_container_width=True, key="btn_sticky"):
            if sticky_msg.strip():
                try:
                    payload = {"text": sticky_msg.strip()}
                    response = requests.put(f"{base_url}sticky/{target}.json", json=payload, timeout=2.0)
                    if response.status_code == 200:
                        st.toast("📌 Đã ghim lời nhắc lên màn hình máy con thành công!", icon="💛")
                    else:
                        st.error("Lỗi đồng bộ dữ liệu lên Firebase.")
                except Exception as e:
                    st.error(f"Lỗi kết nối mạng: {e}")
else: 
    st.info("Không có học sinh trực tuyến để điều khiển.")

st.write("---")

# QR Code Expander
qr_bytes, net_url = generate_network_qr()
if qr_bytes and net_url:
    with st.expander("📲 MÃ QR KẾT NỐI ĐIỆN THOẠI", expanded=False):
        col_qr, col_btn = st.columns([1, 2])
        with col_qr: st.image(qr_bytes, width=150)
        with col_btn:
            st.caption(f"🔗 URL: `{net_url}`")
            st.download_button(label="📥 Tải mã QR", data=qr_bytes, file_name="Ma_QR.png", mime="image/png", key="download_qr_btn")

st.write("---")

# Nhật ký phòng chat công cộng
chats = {}
try:
    res = requests.get(f"{base_url}chats.json", timeout=2)
    if res.status_code == 200 and res.json() and isinstance(res.json(), dict): chats = res.json()
except: pass

all_chats = {**chats, **st.session_state.local_chats}
col_title, col_clear = st.columns([3, 1])
with col_title: st.subheader(f"💬 Nhật ký tin nhắn ({len(all_chats)})")
with col_clear:
    if st.button("🧼 Dọn sạch chat", type="secondary", key="btn_clear_chat"):
        clear_all_chats()
        st.rerun()

if not all_chats: st.info("Chưa có tin nhắn nào.")
else:
    for cid, m in list(all_chats.items())[-15:]:
        if not isinstance(m, dict): continue
        sender = m.get("sender", "Ẩn danh")
        text = m.get("text", "")
        ts = m.get("time", "--:--")
        with st.container(border=True):
            if m.get("type") == "revoked": st.markdown(f"⚠️ *{sender} {text}*")
            else:
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{sender}** <span style='color:gray; font-size:12px;'>({ts})</span>", unsafe_allow_html=True)
                    st.markdown(f"{text}")
                with c2:
                    if st.button("✂️ Gỡ", key=f"del_{cid}", type="primary"):
                        revoke_msg(cid)
                        st.rerun()

st.write("---")
st.text_input("Nội dung lời nhắn công cộng:", value=st.session_state.input_text, key="widget_msg", placeholder="Nhập tin nhắn...", on_change=send_parent_msg)
st.button("Gửi tin nhắn ➤", key="btn_send_msg", on_click=send_parent_msg)
