# -*- coding: utf-8 -*-
"""TEXO – Thiết lập lịch nhắc việc dự án (Recipe 01) trên Google Calendar.
Phòng Kỹ thuật – Công ty CP TEXO Tư vấn và Đầu tư.

Chạy:  streamlit run app.py
"""
import datetime
from datetime import timedelta

import pandas as pd
import streamlit as st

from core import ui
from core.calendar_api import get_calendar_service, get_texo_calendar_id

APP_VERSION = "2.1"
TITLE = "Thiết lập lịch nhắc việc dự án"
ui.setup("TEXO · " + TITLE, "📅")
ui.gate("Thiết lập lịch dự án")

# Mốc 12 tuần đầu: (số ngày từ T+0, mã, nội dung)
MILESTONES = [
    (0, "W01", "Chào mừng & Khởi động dự án"),
    (14, "W02", "Nhắc báo cáo & Thương hiệu"),
    (28, "W04", "Duy trì tiêu chuẩn & Cập nhật TEXO-E"),
    (42, "W06", "Rà soát nhân lực & Năng lực cán bộ"),
    (56, "W08", "Tính đồng bộ của Mẫu biểu & Hồ sơ"),
    (70, "W10", "Hình ảnh thương hiệu & Kiểm soát nội bộ"),
    (84, "W12", "Tổng kết 3 tháng & Định hướng tiếp theo"),
]
RECUR_TITLE = "Kiểm soát Hồ sơ & Số hóa TEXO-E"

# --------------------------------------------------------------------------- thanh bên
with st.sidebar:
    st.markdown("### 📅 Google Calendar")
    try:
        from core import calendar_api
        creds = calendar_api.get_credentials()
        if creds:
            ui.badge("Đã kết nối Google Calendar", "green")
            st.caption("Lịch được tạo vào lịch tên **TEXO** (không có thì dùng lịch cá nhân).")
    except Exception as e:
        st.error(f"⚠️ Cần xác thực: {e}")
        st.stop()
    st.divider()
    ui.logout_button()
    st.caption(f"Thiết lập lịch dự án v{APP_VERSION} · Xây dựng: Hoàng Đức Vũ")

# --------------------------------------------------------------------------- trang chính
ui.header(TITLE, "Phòng Kỹ thuật · Tạo chuỗi mốc nhắc việc trên Google Calendar cho dự án mới – "
                 "12 tuần đầu và định kỳ 6 tháng đến hết tiến độ")

with st.expander("📘 Hướng dẫn sử dụng"):
    st.markdown("""
1. Điền **thông tin hợp đồng** (bắt buộc: Mã HĐ, Trung tâm, Tên dự án) và **tiến độ**.
2. Xem **bảng xem trước** các mốc sẽ tạo bên phải.
3. Bấm **Bắt đầu thiết lập lịch** – app tạo sự kiện cả ngày trên Google Calendar, mô tả sự kiện ghi đủ thông tin hợp đồng.

Tên sự kiện theo chuẩn `Mã HĐ - ttXX - [M-Wxx] - Nội dung`, đồng bộ với Email Milestone Assistant.
Mỗi lần bấm là tạo mới – tránh bấm lặp cho cùng một hợp đồng.
""")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("##### 📋 Thông tin hợp đồng")
    project_code = st.text_input("Mã hợp đồng *", placeholder="Ví dụ: 2026-HĐ-TVGS-01")
    center_id = st.text_input("Trung tâm phụ trách (mã TT) *", placeholder="Ví dụ: TT12")
    project_name = st.text_area("Tên dự án đầy đủ *", placeholder="Ví dụ: Công trình Xây dựng Trụ sở…")
    partner = st.text_input("Đối tác / Chủ đầu tư", placeholder="Ví dụ: Tập đoàn ABC")
    c_a, c_b = st.columns(2)
    service_type = c_a.selectbox("Loại dịch vụ", ["TVGS", "TVQLDA", "Tư vấn Thầu", "Kiểm định", "Khác"])
    value = c_b.text_input("Giá trị hợp đồng (VNĐ)", placeholder="Ví dụ: 1.500.000.000")
    c_c, c_d = st.columns(2)
    project_short = c_c.text_input("Tên viết ngắn", placeholder="Ví dụ: Liền kề Từ Vân")
    location = c_d.text_input("Vị trí dự án", placeholder="Ví dụ: Hà Nội")

    st.markdown("##### ⌚ Tiến độ")
    c_e, c_f = st.columns(2)
    start_date = c_e.date_input("Ngày khởi tạo (T+0)", datetime.date.today(), format="DD/MM/YYYY")
    duration_months = c_f.number_input("Tiến độ dự án (tháng)", min_value=1, value=12)

# Tính trước các mốc để xem trước
center_tag = ""
if center_id:
    center_tag = center_id.lower() if "tt" in center_id.lower() else f"tt{center_id}"
recur_start = start_date + timedelta(days=180)
recur_until = start_date + timedelta(days=duration_months * 30)


def _add_months(day, n):
    """Cộng n tháng như quy tắc lặp của Google Calendar (bỏ qua tháng không có ngày đó)."""
    m = day.month - 1 + n
    y, m = day.year + m // 12, m % 12 + 1
    try:
        return day.replace(year=y, month=m)
    except ValueError:
        return None


recur_dates = []
i = 0
while True:
    d = _add_months(recur_start, 6 * i)
    i += 1
    if d is None:
        continue
    if d > recur_until or i > 60:
        break
    recur_dates.append(d)

with col2:
    st.markdown("##### 🛠 Chế độ thiết lập")
    recipe = st.selectbox("Recipe", ["Recipe 01 (Milestone Sync – 12 tuần)"])
    k = st.columns(3)
    ui.kpi(k[0], len(MILESTONES), "Mốc 12 tuần", "W01 → W12")
    ui.kpi(k[1], len(recur_dates), "Mốc 6 tháng", "đến hết tiến độ" if recur_dates else "tiến độ ≤ 6 tháng",
           "blue" if recur_dates else "grey")
    ui.kpi(k[2], recur_until.strftime("%m/%Y"), "Kết thúc", recur_until.strftime("%d/%m/%Y"))

    st.markdown("**Xem trước các mốc sẽ tạo**")
    rows = [{"Ngày": (start_date + timedelta(days=dd)).strftime("%d/%m/%Y"), "Mã": f"M-{c}", "Nội dung": t}
            for dd, c, t in MILESTONES]
    rows += [{"Ngày": x.strftime("%d/%m/%Y"), "Mã": "M-6M", "Nội dung": RECUR_TITLE + " (lặp 6 tháng)"}
             for x in recur_dates]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True,
                 height=min(38 + 35 * len(rows), 460))
    if project_code:
        st.caption(f"Tên sự kiện mẫu: `{project_code} - {center_tag or 'ttXX'} - [M-W01] - {MILESTONES[0][2]}`")

    missing = [n for n, v in [("Mã HĐ", project_code), ("Trung tâm", center_id), ("Tên dự án", project_name)] if not v]
    if missing:
        ui.callout("🟠 Còn thiếu: <b>" + ", ".join(missing) + "</b> – điền đủ để tạo lịch.", "orange")

    if st.button("📅 Bắt đầu thiết lập lịch", type="primary", use_container_width=True, disabled=bool(missing)):
        with st.spinner("Đang kết nối Google Calendar và tạo chuỗi mốc…"):
            try:
                service = get_calendar_service()
                calendar_id = get_texo_calendar_id(service)
                st.info(f"📍 Đang đồng bộ vào lịch: {calendar_id}")

                desc_template = f"CHI TIẾT HỢP ĐỒNG [{project_code}]\n" + \
                                "----------------------------------\n" + \
                                f"- Mã HĐ: {project_code}\n" + \
                                "- Loại: Hợp đồng\n" + \
                                f"- Đơn vị: Trung tâm {center_id}\n" + \
                                f"- Dịch vụ: {service_type}\n" + \
                                f"- Đối tác: {partner}\n" + \
                                f"- Giá trị: {value} VNĐ\n" + \
                                f"- Dự án: {project_name}\n" + \
                                f"- Tên viết ngắn: {project_short}\n" + \
                                f"- Vị trí: {location}\n" + \
                                f"- Tiến độ: {duration_months} tháng\n" + \
                                "----------------------------------"

                created = []
                for days, code, title in MILESTONES:
                    event_date = start_date + timedelta(days=days)
                    event_title = f"{project_code} - {center_tag} - [M-{code}] - {title}"
                    event = {
                        'summary': event_title,
                        'description': desc_template,
                        'start': {'date': event_date.isoformat()},
                        'end': {'date': (event_date + timedelta(days=1)).isoformat()},
                    }
                    service.events().insert(calendarId=calendar_id, body=event).execute()
                    created.append(f"✅ {event_date.strftime('%d/%m/%Y')} · {event_title}")

                if recur_start < recur_until:
                    recur_title = f"{project_code} - {center_tag} - [M-6M] - {RECUR_TITLE}"
                    rrule = f"RRULE:FREQ=MONTHLY;INTERVAL=6;UNTIL={recur_until.strftime('%Y%m%dT235959Z')}"
                    recurring_event = {
                        'summary': recur_title,
                        'description': desc_template,
                        'start': {'date': recur_start.isoformat(), 'timeZone': 'Asia/Ho_Chi_Minh'},
                        'end': {'date': (recur_start + timedelta(days=1)).isoformat(), 'timeZone': 'Asia/Ho_Chi_Minh'},
                        'recurrence': [rrule],
                    }
                    service.events().insert(calendarId=calendar_id, body=recurring_event).execute()
                    created.append(f"✅ từ {recur_start.strftime('%d/%m/%Y')} lặp 6 tháng · {recur_title}")

                ui.callout(f"🟢 Đã tạo xong <b>{len(created)}</b> sự kiện trên Google Calendar.", "green")
                for line in created:
                    st.write(line)
            except Exception as e:
                st.error(f"❌ Lỗi thiết lập: {e}")
