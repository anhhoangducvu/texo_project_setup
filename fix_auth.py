import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# 1. Cấu hình Scopes và đường dẫn
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDS_FILE = 'credentials.json'

# Để localhost chạy được http (fix lỗi insecure_transport)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def authenticate():
    print(f"\n🚀 ĐANG CẤP QUYỀN TRUY CẬP GOOGLE CALENDAR")
    print("-" * 50)
    
    if not os.path.exists(CREDS_FILE):
        print(f"❌ Lỗi: Không tìm thấy file {CREDS_FILE} tại thư mục này!")
        return
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, CALENDAR_SCOPES)
        creds = flow.run_local_server(port=0, 
                                      authorization_prompt_message="Đăng nhập Google xong đừng tắt màn hình nhé...",
                                      success_message="Xác thực thành công! Bạn có thể quay lại terminal.")
        
        # Lưu ra file local
        token_json = creds.to_json()
        with open('token_calendar.json', 'w') as token:
            token.write(token_json)
        print(f"✅ Đã lưu file: token_calendar.json")
        
        # In ra Secrets
        print(f"\n🔑 CHÌA KHÓA CHO STREAMLIT SECRETS (PROJECT SETUP):")
        print("=" * 60)
        clean_json = json.dumps(json.loads(token_json))
        
        # Lấy thêm google_credentials
        with open(CREDS_FILE, 'r') as f:
            creds_str = json.dumps(json.load(f))

        print(f"calendar_token = '{clean_json}'")
        print(f"google_credentials = '{creds_str}'")
        print("=" * 60)
        print("\n🎉 Xong! Anh Vũ hãy Copy các dòng trên dán vào Secrets để bảo mật GitHub nhé.")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == '__main__':
    authenticate()
    input("\nNhấn Enter để kết thúc...")
