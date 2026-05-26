import streamlit as st
import requests
import time
import socket
import qrcode
import pandas as pd
from io import BytesIO
from datetime import datetime

# ── 🔴 URL FIREBASE GỐC CHUẨN ──
FIREBASE_URL = "https://pomodoroapp-701a2-default-rtdb.firebaseio.com/"

st.set_page_config(page_title="Trung Tâm Điều Khiển Phụ Huynh", page_icon="👑", layout="centered")

if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "local_chats" not in st.session_state:
    st.session_state.local_chats = {}

# --- 📲 HÀM TẠO MÃ QR TỰ ĐỘNG ---
@st.cache_data(ttl=3600)
def generate_network_qr():
    # 🎯 SỬA CHỖ NÀY: Dán chính xác cái link web Streamlit vừa tạo của bạn vào đây!
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
        new_msg = {"sender": "PHỤ HUYNH 👤", "text": msg_text, "time": current_time}
        msg_id = f"local_{int(time.time())}"
        st.session_state.local_chats[msg_id] = new_msg
        
        try:
            base_url = FIREBASE_URL.strip()
            if not base_url.endswith("/"): base_url += "/"
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
            base_url = FIREBASE_URL.strip()
            if not base_url.endswith("/"): base_url += "/"
            requests.patch(f"{base_url}chats/{chat_id}.json", json={"text": "đã bị phụ huynh gỡ bỏ.", "type": "revoked"}, timeout=2)
            st.toast("Đã gỡ tin nhắn trên đám mây!", icon="✂️")
        except: st.toast("Lỗi kết nối mạng!", icon="❌")

# --- 🚨 HÀM PHÁT LỆNH ĐIỀU KHIỂN TỪ XA CHUẨN ĐỒNG BỘ ---
def send_remote_command(payload, target_user):
    try:
        base_url = FIREBASE_URL.strip()
        if not base_url.endswith("/"): base_url += "/"
        requests.put(f"{base_url}commands/{target_user}.json", json=payload, timeout=2)
        st.toast(f"🚨 Đã chuyển lệnh thành công tới {target_user}!", icon="⚡")
    except: st.error("Lỗi kết nối mạng Firebase.")

# --- 🧹 HÀM CLEAR CHAT CỨU HỘ ---
def clear_all_chats():
    try:
        base_url = FIREBASE_URL.strip()
        if not base_url.endswith("/"): base_url += "/"
        res = requests.delete(f"{base_url}chats.json", timeout=2)
        if res.status_code == 200:
            st.session_state.local_chats = {}
            st.toast("🧹 Đã làm sạch phòng chat lỗi!", icon="🧼")
    except: pass

# ── ✨ GIAO DIỆN CHÍNH ✨ ──
st.title("👑 Trung Tâm Quản Lý Phụ Huynh Tối Thượng")

# --- THÔNG TIN TRẠNG THÁI SERVER ---
status_db = "Kết nối tốt 🟢"
try:
    base_url = FIREBASE_URL.strip()
    if not base_url.endswith("/"): base_url += "/"
    res_test = requests.get(f"{base_url}chats.json", timeout=1.5)
    if res_test.status_code != 200: status_db = "Lỗi kết nối 🔴"
except: status_db = "Ngoại tuyến 🟡"

m1, m2, m3 = st.columns(3)
with m1: st.metric(label="📡 Máy chủ Firebase", value=status_db)
with m2: st.metric(label="⏱️ Đồng hồ hệ thống", value=datetime.now().strftime("%H:%M:%S"))
with m3: st.metric(label="💬 Tin nhắc tạm", value=f"{len(st.session_state.local_chats)} tin")

st.write("---")

# 📊 ── BIỂU ĐỒ & THEO DÕI REALTIME ──
st.subheader("📊 Phân Tích & Giám Sát Học Tập")
user_names = []
user_times = []

try:
    res_users = requests.get(f"{base_url}users.json", timeout=2)
    if res_users.status_code == 200 and res_users.json():
        users_data = res_users.json()
        for u_id, u_info in users_data.items():
            if isinstance(u_info, dict):
                u_status = u_info.get("status", "offline")
                u_time = u_info.get("study_seconds", 0) // 60
                user_names.append(u_id)
                user_times.append(u_time)
                status_emoji = "🟢 Trực tuyến" if u_status == "online" else "⚫ Ngoại tuyến"
                st.caption(f"👤 **{u_id}**: {status_emoji} | Đã học: `{u_time} phút`")
        if user_names:
            df = pd.DataFrame({"Học sinh": user_names, "Thời gian học (Phút)": user_times})
            st.bar_chart(data=df, x="Học sinh", y="Thời gian học (Phút)", color="#38bdf8")
    else: st.info("Chưa có dữ liệu học sinh.")
except: st.caption("⚠️ Không thể tải đồ thị giám sát.")

st.write("---")

# ⚡ ── TRUNNG TÂM ĐIỀU KHIỂN TỪ XA ──
st.subheader("⚡ Điều Khiển & Giao Mục Tiêu Từ Xa")
if user_names:
    target = st.selectbox("Chọn con để điều khiển:", user_names)
    
    c_cmd1, c_cmd2 = st.columns(2)
    with c_cmd1:
        if st.button("🔔 PHÁT CHUÔNG CHÚ Ý", use_container_width=True):
            payload = {"command": "ALERT_BUZZ", "timestamp": int(time.time()), "status": "pending"}
            send_remote_command(payload, target)
    with c_cmd2:
        if st.button("🛑 LỆNH NGHỈ NGƠI (KHÓA APP)", type="primary", use_container_width=True):
            payload = {"command": "FORCE_BREAK", "timestamp": int(time.time()), "status": "pending"}
            send_remote_command(payload, target)
            
    st.write("")
    c_target1, c_target2 = st.columns(2)
    with c_target1:
        target_mins = st.number_input("Đặt mục tiêu học hôm nay (Phút):", min_value=5, max_value=180, value=30, step=5)
        if st.button("🚀 Gửi Mục Tiêu Thời Gian", use_container_width=True):
            payload = {
                "command": "SET_GOAL", 
                "minutes": target_mins, 
                "timestamp": int(time.time()), 
                "status": "pending"
            }
            send_remote_command(payload, target)
            
    with c_target2:
        sticky_msg = st.text_input("Lời nhắn ghim màn hình app con:", placeholder="Ví dụ: Học xong nhớ làm bài tập...")
        if st.button("📌 Ghim Lời Nhắc Lên Màn Hình", use_container_width=True):
            if sticky_msg.strip():
                try:
                    base_url = FIREBASE_URL.strip()
                    if not base_url.endswith("/"): base_url += "/"
                    
                    # 🎯 ĐÃ SỬA: Đóng gói đúng cấu trúc khóa "text" và đẩy thẳng vào nhánh "sticky" máy con chờ đợi
                    payload = {"text": sticky_msg.strip()}
                    response = requests.put(f"{base_url}sticky/{target}.json", json=payload, timeout=2.0)
                    
                    if response.status_code == 200:
                        st.toast("📌 Đã ghim lời nhắc lên màn hình máy con thành công!", icon="💛")
                    else:
                        st.error("Lỗi đồng bộ dữ liệu lên Firebase.")
                except Exception as e:
                    st.error(f"Lỗi kết nối mạng: {e}")
else: st.info("Không có học sinh trực tuyến để điều khiển.")

st.write("---")

# QR Code Expander
qr_bytes, net_url = generate_network_qr()
if qr_bytes and net_url:
    with st.expander("📲 MÃ QR KẾT NỐI ĐIỆN THOẠI", expanded=False):
        col_qr, col_btn = st.columns([1, 2])
        with col_qr: st.image(qr_bytes, width=150)
        with col_btn:
            st.caption(f"🔗 URL: `{net_url}`")
            st.download_button(label="📥 Tải mã QR", data=qr_bytes, file_name="Ma_QR.png", mime="image/png")

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
    if st.button("🧼 Dọn sạch chat", type="secondary"):
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

# Vòng lặp đếm ngược đồng bộ dữ liệu
progress_bar = st.progress(0, text="🔄 Chuẩn bị đồng bộ dữ liệu...")
for percent_complete in range(100):
    time.sleep(0.05)
    progress_bar.progress(percent_complete + 1, text=f"🔄 Đang đồng bộ tự động... {5 - (percent_complete*5//100)}s")
st.rerun()
