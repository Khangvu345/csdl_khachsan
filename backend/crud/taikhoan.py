from db import get_db_connection

def get_by_username(tendangnhap: str):
    """
    Tìm tài khoản trong CSDL bằng Tên Đăng Nhập.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM TAIKHOAN WHERE TenDangNhap = %s"
            cursor.execute(sql, (tendangnhap,))
            taikhoan = cursor.fetchone()
            return taikhoan
    except Exception as e:
        print(f"Lỗi truy vấn CSDL: {e}")
        return None
    finally:
        if conn:
            conn.close()
