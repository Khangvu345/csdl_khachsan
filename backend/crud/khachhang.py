from db import get_db_connection
from schemas import khachhang as khachhang_schema


def create(kh: khachhang_schema.KhachHangCreate):
    """Thêm một khách hàng mới vào CSDL."""
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            # Dùng transaction để đảm bảo cả hai lệnh insert đều thành công
            conn.begin()

            # 1. Thêm vào bảng KHACHHANG
            sql_kh = "INSERT INTO KHACHHANG (MaKH, Ho, Ten, TenDem, Email, DiaChi) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_kh, (kh.MaKH, kh.Ho, kh.Ten, kh.TenDem, kh.Email, kh.DiaChi))

            # 2. Thêm SĐT vào bảng SDT_KHACHHANG
            sql_sdt = "INSERT INTO SDT_KHACHHANG (MaKH, SDT) VALUES (%s, %s)"
            cursor.execute(sql_sdt, (kh.MaKH, kh.SDT))

            conn.commit()
            return kh.dict(), None
    except Exception as e:
        conn.rollback()
        # Trả về lỗi nếu MaKH hoặc Email bị trùng lặp
        if "Duplicate entry" in str(e):
            return None, "Mã khách hàng hoặc Email đã tồn tại."
        return None, str(e)
    finally:
        conn.close()


def get_all():
    """Lấy danh sách tất cả khách hàng."""
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            # Query để lấy thông tin khách hàng và tổng hợp các SĐT của họ
            sql = """
                SELECT k.*, GROUP_CONCAT(s.SDT SEPARATOR ', ') as SDT
                FROM KHACHHANG k
                LEFT JOIN SDT_KHACHHANG s ON k.MaKH = s.MaKH
                GROUP BY k.MaKH
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            # Chuyển đổi chuỗi SDT thành danh sách
            for row in result:
                if row['SDT']:
                    row['SDT'] = row['SDT'].split(', ')
                else:
                    row['SDT'] = []
            return result, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()


def get_by_id(makh: str):
    """Lấy thông tin một khách hàng theo MaKH."""
    # Tương tự hàm get_all nhưng có thêm điều kiện WHERE k.MaKH = %s
    # (Để ngắn gọn, phần này sẽ được triển khai tương tự get_all)
    pass  # Bạn có thể tự triển khai phần này

# --- Code đã được sửa lỗi ---
def update(makh: str, kh_update: khachhang_schema.KhachHangUpdate):
    """Cập nhật thông tin khách hàng."""
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            conn.begin()

            # SỬA Ở ĐÂY: Thêm Ho, Ten, TenDem vào câu lệnh UPDATE
            sql_kh = """
                UPDATE KHACHHANG 
                SET Ho = %s, TenDem = %s, Ten = %s, Email = %s, DiaChi = %s 
                WHERE MaKH = %s
            """
            cursor.execute(sql_kh, (
                kh_update.Ho,
                kh_update.TenDem,
                kh_update.Ten,
                kh_update.Email,
                kh_update.DiaChi,
                makh
            ))

            # Lưu ý: Logic cập nhật SĐT này vẫn còn đơn giản.
            # Nếu một khách hàng có thể có nhiều SĐT, bạn sẽ cần một logic phức tạp hơn.
            # Tạm thời, chúng ta giữ nguyên để sửa lỗi trước mắt.
            if kh_update.SDT:
                # Kiểm tra xem khách hàng đã có SĐT chưa
                cursor.execute("SELECT 1 FROM SDT_KHACHHANG WHERE MaKH = %s", (makh,))
                if cursor.fetchone():
                    # Nếu có rồi -> UPDATE
                    sql_sdt = "UPDATE SDT_KHACHHANG SET SDT = %s WHERE MaKH = %s LIMIT 1"
                    cursor.execute(sql_sdt, (kh_update.SDT, makh))
                else:
                    # Nếu chưa có -> INSERT
                    sql_sdt = "INSERT INTO SDT_KHACHHANG (MaKH, SDT) VALUES (%s, %s)"
                    cursor.execute(sql_sdt, (makh, kh_update.SDT))


            conn.commit()
            return {"message": "Cập nhật thành công"}, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        if conn:
            conn.close()

def delete(makh: str):
    """Xóa một khách hàng."""
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            # **Quan trọng**: Kiểm tra xem khách hàng có đặt phòng nào không trước khi xóa
            sql_check = "SELECT 1 FROM DATPHONG WHERE MaKH = %s LIMIT 1"
            cursor.execute(sql_check, (makh,))
            if cursor.fetchone():
                return None, "Không thể xóa khách hàng vì đã có lịch sử đặt phòng."

            # Nếu không có đặt phòng, tiến hành xóa
            # Do có `ON DELETE CASCADE`, SĐT trong SDT_KHACHHANG sẽ tự động bị xóa
            sql_delete = "DELETE FROM KHACHHANG WHERE MaKH = %s"
            result = cursor.execute(sql_delete, (makh,))

            if result == 0:
                return None, "Không tìm thấy khách hàng để xóa."

            conn.commit()
            return {"message": "Xóa khách hàng thành công"}, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        conn.close()