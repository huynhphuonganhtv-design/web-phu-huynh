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
            background-color: #1e293b !important; border: 1px solid #334155 !important;
            border-radius: 14px !important; padding: 22px !important;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3) !important;
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px); border-color: #38bdf8 !important;
            box-shadow: 0 15px 25px -5px rgba(56,189,248,0.15) !important;
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
            0% { box-shadow: 0 0 0 0 rgba(239,68,68,0.4); }
            70% { box-shadow: 0 0 0 10px rgba(239,68,68,0); }
            100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
        }
        button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #ef4444, #b91c1c) !important; border: none !important; color: white !important; font-weight: bold !important;
            border-radius: 8px !important; transition: all 0.25s ease-in-out !important; animation: pulse-red 2s infinite;
        }
        button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #38bdf8, #2563eb) !important; color: white !important; font-weight: bold !important; border: none !important;
            border-radius: 8px !important; transition: all 0.25s ease-in-out !important;
        }
        button[data-testid="baseButton-secondary"]:hover { transform: translateY(-1px); box-shadow: 0 0 15px rgba(56,189,248,0.6) !important; }
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
            background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 14px !important; padding: 22px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
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
    if st.button("🔒 Đăng xuất ứng dụng", width="stretch"):
        st.session_state["authenticated"] = False
        st.rerun()

# Đồng hồ
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

    # KPI Cards
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
            
            # Tính toán tỷ lệ phần trăm %
            progress_pct = min(1.0, today_mins / max(1, target_goal_mins))
            percent_val = int(progress_pct * 100)
            
            # THUẬT TOÁN ĐỔI MÀU TỰ ĐỘNG DỰA TRÊN % ĐẠT ĐƯỢC
            if percent_val < 40:
                bar_color = "#ef4444"  # Màu Đỏ (Cần cố gắng thêm)
            elif percent_val < 80:
                bar_color = "#f59e0b"  # Màu Vàng (Sắp hoàn thành rồi)
            else:
                bar_color = "#22c55e"  # Màu Xanh Lá (Xuất sắc đạt mục tiêu)
                
            # Tạo thanh Progress Bar HTML tùy biến màu sắc
            st.markdown(f"""
                <div style="width: 100%; background-color: #334155; border-radius: 8px; height: 18px; margin: 4px 0;">
                    <div style="width: {percent_val}%; background-color: {bar_color}; height: 100%; border-radius: 8px; transition: width 0.5s ease-in-out;"></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.caption(f"📈 Đã hoàn thành **{percent_val}%** ({today_mins}/{target_goal_mins} phút theo mục tiêu từ cha mẹ).")
            st.write("")

    tab1, tab1_th, tab2, tab3, tab4 = st.tabs([
        "📅 Theo ngày (30 ngày)",
        "📈 Xu hướng (TH)", 
        "🥧 Theo môn học",
        "🏆 So sánh học sinh",
        "🗓️ Lịch sử gần đây"
    ])

    # TAB 1 — Chuỗi ngày học liên tiếp chuẩn thuật toán thực tế
    with tab1:
        if all_daily:
            sorted_days = sorted(all_daily.items())
            last_30_days = sorted_days[-30:]
            labels_d = [d[0][-5:] for d in last_30_days]
            values_d = [d[1] for d in last_30_days]
            avg_v    = sum(values_d) / max(len(values_d), 1)

            chart_color = "#38bdf8" if st.session_state["theme_mode"] == "🌙 Giao diện Tối" else "#0284c7"
            chart_data_d = pd.DataFrame({"Ngày": labels_d, "Phút học": values_d}).set_index("Ngày")
            st.bar_chart(chart_data_d, color=chart_color)

            col_a, col_b, col_c = st.columns(3)
            col_a.metric("🔥 Ngày học nhiều nhất", f"{max(values_d)} phút")
            col_b.metric("📈 Trung bình 30 ngày",   f"{int(avg_v)} phút")
            col_c.metric("✅ Ngày có học",           f"{sum(1 for v in values_d if v > 0)}/30 ngày")

            # --- THUẬT TOÁN TÍNH CHUỖI STREAK LIÊN TIẾP CHUẨN XÁC ---
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

            # Hiển thị vinh danh chuỗi ngày học
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

    # TAB 1_TH — BIỂU ĐỒ XU HƯỚNG REALTIME
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

    # TAB 2 — Theo môn học
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

    # TAB 3 — So sánh học sinh
    with tab3:
        if student_totals:
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
                st.success(f"🎉 **{winner['Học sinh']}** đang dẫn đầu với {winner['Tổng phút']} phút, hơn người thứ 2 {gap} phút!")
        else:
            st.info("Chưa có dữ liệu học sinh để so sánh.")

    # TAB 4 — Lịch sử phiên học
    with tab4:
            if all_history:
                # 1. Tự động lấy danh sách các môn học hiện có trong lịch sử (bỏ trùng)
                unique_subjects = sorted(list(set([h.get("subject", "Không rõ") for h in all_history if h.get("subject")])))
                
                # 2. Tạo dropdown chọn môn học
                selected_sub = st.selectbox(
                    "🎯 Xem riêng lịch sử môn học:", 
                    ["📚 Tất cả các môn"] + unique_subjects, 
                    key="filter_subject_box_ultimate"
                )
                
                # 3. Tiến hành lọc dữ liệu dựa trên lựa chọn
                filtered_history = all_history
                if selected_sub != "📚 Tất cả các môn":
                    filtered_history = [h for h in all_history if h.get("subject") == selected_sub]
                
                # 4. Sắp xếp và lấy 20 phiên gần nhất CỦA MÔN ĐÓ
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
                    
                    # 5. Tính toán số liệu thống kê động theo bộ lọc
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
        target_mins = st.number_input("Đặt mục tiêu học hôm nay (Phút):", min_value=5, max_value=180, value=30, step=5)
        if st.button("🚀 Gửi Mục Tiêu Thời Gian", width="stretch"):
            send_remote_command({"command": "SET_GOAL", "minutes": target_mins, "timestamp": int(time.time()), "status": "pending"}, target)
    with c_target2:
        sticky_msg = st.text_input("Lời nhắn ghim màn hình app con:", placeholder="Nhập tin nhắn nhắn nhủ...")
        if st.button("📌 Ghim Lời Nhắc", width="stretch"):
            if sticky_msg.strip():
                requests.put(f"{base_url}sticky/{target}.json", json={"text": sticky_msg.strip()}, timeout=2)

st.write("---")

# QR Code
qr_bytes, net_url = generate_network_qr()
if qr_bytes:
    with st.expander("📲 MÃ QR KẾT NỐI ĐIỆN THOẠI"):
        st.image(qr_bytes, width=150)
        st.caption(f"🔗 Link: `{net_url}`")
        st.download_button(
            label="📥 Tải mã QR về máy",
            data=qr_bytes,
            file_name="qrcode_phuhuynh.png",
            mime="image/png",
            width="stretch",
            type="secondary"
        )

# =====================================================================
# 💬 PHÒNG CHAT
# =====================================================================
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
                if st.button("✂️ Gỡ tin nhắn", key=f"del_{cid}", type="primary", width="stretch"):
                    revoke_msg(cid)
                    st.rerun()

st.text_input("Nội dung lời nhắn công cộng:", key="widget_msg", placeholder="Nhập tin nhắn...", on_change=send_parent_msg)
st.button("Gửi tin nhắn ➤", key="btn_send_msg", on_click=send_parent_msg, width="stretch", type="secondary")
