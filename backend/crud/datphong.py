from db import get_db_connection
from schemas import datphong as datphong_schema
from typing import Optional
from datetime import date


def create(dp: datphong_schema.DatPhongCreate):
    """Tạo một lượt đặt phòng mới và cập nhật trạng thái phòng."""
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            conn.begin()  # Bắt đầu transaction

            # 1. Kiểm tra phòng có sẵn sàng không
            sql_check_phong = "SELECT TinhTrang FROM PHONG WHERE MaPhong = %s"
            cursor.execute(sql_check_phong, (dp.MaPhong,))
            phong = cursor.fetchone()
            if not phong or phong['TinhTrang'] != 'Trống':
                conn.rollback()
                return None, "Phòng không có sẵn hoặc không tồn tại."

            # 2. Thêm vào bảng DATPHONG
            sql_insert_dp = """
                INSERT INTO DATPHONG (MaDatPhong, NgayNhanPhong, NgayTraPhong, TrangThaiDatPhong, MaKH, MaPhong)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert_dp, (
                dp.MaDatPhong, dp.NgayNhanPhong, dp.NgayTraPhong,
                dp.TrangThaiDatPhong, dp.MaKH, dp.MaPhong
            ))

            # 3. Cập nhật trạng thái phòng thành 'Đã đặt'
            # SỬA LỖI Ở ĐÂY: Bỏ chữ "được" để tuân thủ CHECK constraint
            sql_update_phong = "UPDATE PHONG SET TinhTrang = 'Đã đặt' WHERE MaPhong = %s"
            cursor.execute(sql_update_phong, (dp.MaPhong,))

            conn.commit()  # Hoàn tất transaction
            return dp.dict(), None
    except Exception as e:
        conn.rollback()
        # Trả về lỗi CSDL để frontend có thể hiển thị
        return None, str(e)
    finally:
        if conn:
            conn.close()


def get_all_detailed(trang_thai: Optional[str], ngay: Optional[date]):
    """
    Lấy danh sách chi tiết các lượt đặt phòng, bao gồm cả tên khách hàng và tên phòng.
    """
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            base_sql = """
                SELECT
                    dp.MaDatPhong, dp.NgayNhanPhong, dp.NgayTraPhong,
                    dp.TrangThaiDatPhong, dp.MaKH, dp.MaPhong,
                    p.MaPhong AS TenPhong, 
                    CONCAT(k.Ho, ' ', IFNULL(k.TenDem, ''), ' ', k.Ten) AS TenKhachHang
                FROM DATPHONG dp
                JOIN KHACHHANG k ON dp.MaKH = k.MaKH
                JOIN PHONG p ON dp.MaPhong = p.MaPhong
            """
            conditions = []
            params = []

            if trang_thai:
                conditions.append("dp.TrangThaiDatPhong = %s")
                params.append(trang_thai)
            if ngay:
                conditions.append("%s BETWEEN dp.NgayNhanPhong AND dp.NgayTraPhong")
                params.append(ngay)

            if conditions:
                base_sql += " WHERE " + " AND ".join(conditions)

            cursor.execute(base_sql, tuple(params))
            result = cursor.fetchall()
            return result, None
    except Exception as e:
        return None, str(e)
    finally:
        if conn:
            conn.close()


def update(madatphong: str, dp_update: datphong_schema.DatPhongUpdate):
    """
    Cập nhật thông tin một lượt đặt phòng.
    """
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            sql = "UPDATE DATPHONG SET NgayNhanPhong = %s, NgayTraPhong = %s WHERE MaDatPhong = %s"
            result = cursor.execute(sql, (
                dp_update.NgayNhanPhong,
                dp_update.NgayTraPhong,
                madatphong
            ))

            if result == 0:
                conn.rollback()
                return None, "Không tìm thấy đặt phòng để cập nhật."

            conn.commit()
            return {"message": "Cập nhật đặt phòng thành công"}, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        if conn:
            conn.close()


def cancel(madatphong: str):
    """Hủy một lượt đặt phòng và cập nhật lại trạng thái phòng."""
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            conn.begin()

            sql_get_phong = "SELECT MaPhong, TrangThaiDatPhong FROM DATPHONG WHERE MaDatPhong = %s"
            cursor.execute(sql_get_phong, (madatphong,))
            datphong = cursor.fetchone()

            if not datphong:
                conn.rollback()
                return None, "Mã đặt phòng không tồn tại."
            if datphong['TrangThaiDatPhong'] != 'Đã đặt':
                conn.rollback()
                return None, f"Chỉ có thể hủy các đặt phòng có trạng thái 'Đã đặt'."

            sql_update_dp = "UPDATE DATPHONG SET TrangThaiDatPhong = 'Đã hủy' WHERE MaDatPhong = %s"
            cursor.execute(sql_update_dp, (madatphong,))

            ma_phong = datphong['MaPhong']
            sql_update_phong = "UPDATE PHONG SET TinhTrang = 'Trống' WHERE MaPhong = %s"
            cursor.execute(sql_update_phong, (ma_phong,))

            conn.commit()
            return {"message": f"Đã hủy thành công đặt phòng {madatphong}"}, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        if conn:
            conn.close()