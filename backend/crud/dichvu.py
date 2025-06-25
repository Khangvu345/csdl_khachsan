from db import get_db_connection
from schemas import dichvu as dichvu_schema


def assign_service(detail: dichvu_schema.ChiTietDichVuCreate):
    """
    Gán một dịch vụ vào một lượt đặt phòng trong CSDL.
    """
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            # Câu lệnh INSERT vào bảng liên kết
            sql = "INSERT INTO CHI_TIET_DICH_VU (MaDatPhong, MaDV) VALUES (%s, %s)"
            cursor.execute(sql, (detail.MaDatPhong, detail.MaDV))
            conn.commit()
            return detail.dict(), None
    except Exception as e:
        conn.rollback()
        # Bắt các lỗi thường gặp
        if "Duplicate entry" in str(e):
            return None, "Dịch vụ này đã được gán cho đặt phòng."
        if "foreign key constraint fails" in str(e):
            # Lỗi này xảy ra khi MaDatPhong hoặc MaDV không tồn tại trong các bảng tương ứng
            return None, "Mã đặt phòng hoặc mã dịch vụ không hợp lệ."
        return None, str(e)
    finally:
        if conn:
            conn.close()


def get_services_by_booking_id(madatphong: str):
    """
    Lấy danh sách các dịch vụ đã được gán cho một Mã Đặt Phòng.
    """
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            # Query JOIN hai bảng để lấy thông tin chi tiết của dịch vụ
            sql = """
                SELECT dv.MaDV, dv.TenDV, dv.GiaDV
                FROM CHI_TIET_DICH_VU ctdv
                JOIN DICHVU dv ON ctdv.MaDV = dv.MaDV
                WHERE ctdv.MaDatPhong = %s
            """
            cursor.execute(sql, (madatphong,))
            result = cursor.fetchall()
            return result, None
    except Exception as e:
        return None, str(e)
    finally:
        if conn:
            conn.close()
