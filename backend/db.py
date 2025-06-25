import pymysql
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
# Giúp bảo mật thông tin nhạy cảm như mật khẩu CSDL
load_dotenv()

def get_db_connection():
    """
    Tạo và trả về một kết nối đến CSDL MySQL.
    Sử dụng các biến môi trường để lấy thông tin kết nối.
    """
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "HocSQL@155@"), # THAY bằng mật khẩu của bạn
            database=os.getenv("DB_NAME", "qlks"),
            # Rất quan trọng: Trả về kết quả dưới dạng dictionary (object) thay vì tuple
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.MySQLError as e:
        # Ghi lại lỗi nếu không thể kết nối
        print(f"Lỗi không thể kết nối đến MySQL: {e}")
        return None
