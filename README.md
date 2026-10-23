# 📅 Thiết lập lịch nhắc việc dự án – TEXO (Recipe 01) – v2.1

Tự động hóa thiết lập các mốc Milestone đồng bộ cho dự án mới trên Google Calendar.

## ✨ Tính năng
- Thiết lập 07 Milestone trong 12 tuần đầu (W1 -> W12).
- Thiết lập 01 Milestone dài kỳ lặp lại mỗi 6 tháng.
- Tự động điền đầy đủ thông tin hợp đồng vào phần mô tả sự kiện.
- Đồng bộ hoàn toàn với **Email Milestone Assistant**.

## Bản 2.1 – đồng bộ giao diện
- Đăng nhập và giao diện đồng bộ với bộ app Phòng Kỹ thuật: đăng nhập gọn có logo TEXO, đầu trang logo + tiêu đề, nút Đăng xuất, giao diện sáng cố định (`.streamlit/config.toml`).
- Thêm ô tổng hợp (số mốc 12 tuần, số mốc 6 tháng, ngày kết thúc) và **bảng xem trước** các mốc trước khi tạo lịch.
- Nút tạo lịch chỉ bấm được khi đã điền Mã HĐ, Trung tâm, Tên dự án.
- Mật khẩu mặc định `texo2026`, đổi bằng `APP_PASSWORD` trong Secrets.
- Giao diện dùng chung ở `core/ui.py`, logo ở `assets/logo_texo.png`.

## 🚀 Cài đặt
1. Cài đặt thư viện: `pip install -r requirements.txt`
2. Chuẩn bị `credentials.json` (Google Cloud Console).
3. Chạy ứng dụng: `streamlit run app.py`

---
_Người xây dựng: Hoàng Đức Vũ – Phòng Kỹ thuật._
