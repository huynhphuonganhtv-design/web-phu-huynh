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

# 🔥 TÙY BIẾN GIAO DIỆN TỐI (DARK MODE CSS) SIÊU ĐẸP
st.markdown("""
    <style>
    /* Nền tổng thể và font chữ */
    .stApp {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    /* Làm đẹp các khung chứa container */
    [data-testid="stHeader"] {
        background-color: rgba(15, 23, 42, 0.8);
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    /* Tùy chỉnh màu sắc tiêu đề và văn bản */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    /* Định dạng lại Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid #1e293b;
    }
    /* Làm đẹp các ô nhập liệu đầu vào */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #0f172a !important;
        color: #f1f5f9 !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    /* Nút bấm đặc biệt (Primary) - Màu đỏ cảnh báo */
    button[data-testid="baseButton-primary"] {
        background-color: #ef4444 !important;
        border-color: #ef4444 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    button[data-testid="baseButton-primary"]:hover {
        background-color: #dc2626 !important;
        box-shadow: 0 0 12px #ef4444;
    }
    /* Nút bấm thông thường (Secondary) - Màu xanh Neon */
    button[data-testid="baseButton-secondary"] {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #7dd3fc !important;
        box-shadow: 0 0 12px #38bdf8;
    }
    </style>
""", unsafe_allow_html=True)

# Xử lý chuẩn hóa URL Firebase
base_url = FIREBASE_URL.strip()
if not base_url.endswith("/"): base_url += "/"

# Khởi tạo các biến trạng thái nếu chưa có
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
if user_names:
    df = pd.DataFrame({"Học sinh": user_names, "Thời gian học (Phút)": user_times})
    st.bar_chart(data=df, x="Học sinh", y="Thời gian học (Phút)", color="#38bdf8")
else:
    st.info("Biểu đồ trống: Đang chờ máy con kết nối...")

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
