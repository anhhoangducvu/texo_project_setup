import streamlit as st
import datetime
from datetime import timedelta
from core.calendar_api import get_calendar_service

# --- CONFIG ---
st.set_page_config(page_title="TEXO Project Setup", page_icon="🚀", layout="wide")

# --- STYLE PREMIUM ---
st.markdown("""
<style>
    .stApp { background-color: #0A1931 !important; color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6, p, span, div, li, label, .stMarkdown { color: #ffffff !important; }
    .main-header { color: #FFD700 !important; font-weight: 800; font-size: 32px; text-align: center; border-bottom: 2px solid #FFD700; padding-bottom: 10px; margin-bottom: 20px; }
    [data-testid="stSidebar"] { background-color: #050C1A !important; border-right: 1px solid #FFD700; }
    .stButton>button { background: #152A4A !important; color: #FFD700 !important; border: 1px solid #FFD700 !important; border-radius: 12px; font-weight: bold; height: 3.5em; width: 100%; }
    .stButton>button:hover { background: #FFD700 !important; color: #0A1931 !important; transform: scale(1.02); transition: 0.2s; }
    .stSelectbox div[data-baseweb="select"] { background-color: #152A4A !important; color: white !important; }
    .footer { text-align: center; color: #888; font-size: 12px; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# --- AUTH ---
def check_password():
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if st.session_state.authenticated: return True
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #FFD700;'>🚀 PENTAGON SETUP CENTER</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Mật khẩu truy cập:", type="password")
        if st.button("KÍCH HOẠT HỆ THỐNG"):
            if pwd == "texo2026":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("❌ Truy cập không hợp lệ.")
    return False

if not check_password(): st.stop()

# --- MAIN ---
st.markdown("<div class='main-header'>🚀 THIẾT LẬP DỰ ÁN MỚI - RECIPE 01</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📋 Thông tin Hợp đồng")
    project_code = st.text_input("Mã Hợp đồng (Mã HĐ):", placeholder="Ví dụ: 2026-HĐ-TVGS-01")
    center_id = st.text_input("Trung tâm phụ trách (Mã TT):", placeholder="Ví dụ: TT12")
    project_name = st.text_area("Tên dự án đầy đủ:", placeholder="Ví dụ: Công trình Xây dựng Trụ sở...")
    partner = st.text_input("Đối tác / Chủ đầu tư:", placeholder="Ví dụ: Tập đoàn ABC")
    value = st.text_input("Giá trị hợp đồng (VNĐ):", placeholder="Ví dụ: 5.000.000.000 VNĐ")
    
    st.markdown("### ⌚ Tiến độ")
    start_date = st.date_input("Ngày khởi tạo (T+0):", datetime.date.today())
    duration_months = st.number_input("Tiến độ dự án (Tháng):", min_value=1, value=12)

with col2:
    st.markdown("### 🛠 Chế độ Thiết lập")
    recipe = st.selectbox("Chọn Recipe:", ["Recipe 01 (Milestone Sync - 12 Tuần)"])
    st.info("💡 Recipe 01 sẽ tự động tạo 07 sự kiện trong 12 tuần đầu và 01 sự kiện lập lại mỗi 6 tháng.")
    
    if st.button("🚀 BẮT ĐẦU THIẾT LẬP LỊCH"):
        if not project_code or not center_id or not project_name:
            st.error("❌ Vui lòng điền đầy đủ các thông tin bắt buộc (Mã HĐ, TT, Tên dự án).")
        else:
            with st.spinner("Đang kết nối Google Calendar và khởi tạo chuỗi Milestones..."):
                try:
                    service = get_calendar_service()
                    
                    # 1. Milestone Map
                    milestones = [
                        (0, "W01", "Chào mừng & Khởi động dự án"),
                        (14, "W02", "Nhắc báo cáo & Thương hiệu"),
                        (28, "W04", "Duy trì tiêu chuẩn & Cập nhật TEXO-E"),
                        (42, "W06", "Rà soát nhân lực & Năng lực cán bộ"),
                        (56, "W08", "Tính đồng bộ của Mẫu biểu & Hồ sơ"),
                        (70, "W10", "Hình ảnh thương hiệu & Kiểm soát nội bộ"),
                        (84, "W12", "Tổng kết 3 tháng & Định hướng tiếp theo"),
                    ]
                    
                    desc_template = f"CHI TIẾT HỢP ĐỒNG {project_code}\n" + \
                                   "----------------------------------\n" + \
                                   f"- Đơn vị phụ trách: {center_id}\n" + \
                                   f"- Dự án: {project_name}\n" + \
                                   f"- Đối tác: {partner}\n" + \
                                   f"- Giá trị: {value}\n" + \
                                   f"- Tiến độ: {duration_months} Tháng\n" + \
                                   "- Liên hệ: Bà Lê Phương Ly - Trưởng P.HCTH\n" + \
                                   "----------------------------------"

                    # Create Single Events
                    for days, code, title in milestones:
                        event_date = start_date + timedelta(days=days)
                        event_title = f"{project_code} - [M-{code}] - {title}"
                        
                        event = {
                            'summary': event_title,
                            'description': desc_template,
                            'start': {'date': event_date.isoformat()},
                            'end': {'date': (event_date + timedelta(days=1)).isoformat()},
                        }
                        service.events().insert(calendarId='primary', body=event).execute()
                        st.write(f"✅ Đã tạo: {event_title} ({event_date})")

                    # Create Recurring Event (6 months)
                    recur_start = start_date + timedelta(days=180)
                    recur_until = start_date + timedelta(days=duration_months * 30)
                    
                    if recur_start < recur_until:
                        recur_title = f"{project_code} - [M-6M] - Kiểm duyệt Hồ sơ & Số hóa TEXO-E"
                        rrule = f"RRULE:FREQ=MONTHLY;INTERVAL=6;UNTIL={recur_until.strftime('%Y%m%dT235959Z')}"
                        
                        recurring_event = {
                            'summary': recur_title,
                            'description': desc_template,
                            'start': {'date': recur_start.isoformat(), 'timeZone': 'Asia/Ho_Chi_Minh'},
                            'end': {'date': (recur_start + timedelta(days=1)).isoformat(), 'timeZone': 'Asia/Ho_Chi_Minh'},
                            'recurrence': [rrule],
                        }
                        service.events().insert(calendarId='primary', body=recurring_event).execute()
                        st.write(f"✅ Đã tạo chu kỳ 6 tháng: {recur_title}")
                    
                    st.success("🎉 TẤT CẢ LỊCH ĐÃ ĐƯỢC THIẾT LẬP THÀNH CÔNG!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Lỗi thiết lập: {e}")

st.markdown("<div class='footer'>TEXO Engineering Department | Milestone Sync Intelligence | Hoàng Đức Vũ</div>", unsafe_allow_html=True)
