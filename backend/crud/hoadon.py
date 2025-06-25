from db import get_db_connection
from schemas import hoadon as hoadon_schema
from datetime import date


def create_invoice(hd_request: hoadon_schema.HoaDonCreateRequest):
    """
    Tạo hóa đơn, tính tổng tiền, và cập nhật trạng thái đặt phòng & phòng.
    Đây là một transaction phức tạp để đảm bảo toàn vẹn dữ liệu.
    """
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            # === BẮT ĐẦU TRANSACTION ===
            conn.begin()

            # 1. KIỂM TRA TRẠNG THÁI ĐẶT PHÒNG
            sql_check_status = "SELECT MaPhong, TrangThaiDatPhong FROM DATPHONG WHERE MaDatPhong = %s"
            cursor.execute(sql_check_status, (hd_request.MaDatPhong,))
            datphong = cursor.fetchone()
            if not datphong:
                conn.rollback()
                return None, "Mã đặt phòng không tồn tại."
            if datphong['TrangThaiDatPhong'] != 'Đã đặt':
                conn.rollback()
                return None, f"Không thể lập hóa đơn cho đặt phòng có trạng thái '{datphong['TrangThaiDatPhong']}'."

            # 2. TÍNH TỔNG TIỀN HÓA ĐƠN
            sql_calculate_total = """
                SELECT 
                    (DATEDIFF(dp.NgayTraPhong, dp.NgayNhanPhong) * p.GiaPhong) + 
                    (SELECT IFNULL(SUM(dv.GiaDV), 0) 
                     FROM CHI_TIET_DICH_VU ctdv 
                     JOIN DICHVU dv ON ctdv.MaDV = dv.MaDV 
                     WHERE ctdv.MaDatPhong = dp.MaDatPhong) AS TongTien
                FROM DATPHONG dp
                JOIN PHONG p ON dp.MaPhong = p.MaPhong
                WHERE dp.MaDatPhong = %s;
            """
            cursor.execute(sql_calculate_total, (hd_request.MaDatPhong,))
            total_result = cursor.fetchone()
            tong_tien = total_result['TongTien'] if total_result else 0.0

            # 3. INSERT VÀO BẢNG HÓA ĐƠN
            ngay_lap_hoa_don = date.today()
            sql_insert_hd = """
                INSERT INTO HOADON (MaHoaDon, NgayLapHoaDon, TongTienHoaDon, PhuongThucThanhToan, MaNV, MaDatPhong)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert_hd, (
                hd_request.MaHoaDon, ngay_lap_hoa_don, tong_tien,
                hd_request.PhuongThucThanhToan, hd_request.MaNV, hd_request.MaDatPhong
            ))

            # 4. CẬP NHẬT TRẠNG THÁI ĐẶT PHÒNG THÀNH 'Hoàn tất'
            sql_update_dp = "UPDATE DATPHONG SET TrangThaiDatPhong = 'Hoàn tất' WHERE MaDatPhong = %s"
            cursor.execute(sql_update_dp, (hd_request.MaDatPhong,))

            # 5. CẬP NHẬT TRẠNG THÁI PHÒNG THÀNH 'Trống'
            ma_phong = datphong['MaPhong']
            sql_update_phong = "UPDATE PHONG SET TinhTrang = 'Trống' WHERE MaPhong = %s"
            cursor.execute(sql_update_phong, (ma_phong,))

            # === KẾT THÚC TRANSACTION ===
            conn.commit()

            created_invoice = hoadon_schema.HoaDon(
                MaHoaDon=hd_request.MaHoaDon, NgayLapHoaDon=ngay_lap_hoa_don, TongTienHoaDon=tong_tien,
                PhuongThucThanhToan=hd_request.PhuongThucThanhToan, MaNV=hd_request.MaNV,
                MaDatPhong=hd_request.MaDatPhong
            )
            return created_invoice, None

    except Exception as e:
        conn.rollback()
        if "Duplicate entry" in str(e):
            return None, "Mã hóa đơn đã tồn tại."
        return None, str(e)
    finally:
        if conn:
            conn.close()


# --- THÊM HÀM MỚI ---
def get_all():
    """Lấy danh sách chi tiết tất cả các hóa đơn."""
    conn = get_db_connection()
    if not conn:
        return None, "Lỗi kết nối CSDL"

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT 
                    hd.*,
                    dp.MaPhong,
                    nv.TenNV AS TenNhanVien,
                    CONCAT(k.Ho, ' ', IFNULL(k.TenDem, ''), ' ', k.Ten) AS TenKhachHang
                FROM HOADON hd
                JOIN NHANVIEN nv ON hd.MaNV = nv.MaNV
                JOIN DATPHONG dp ON hd.MaDatPhong = dp.MaDatPhong
                JOIN KHACHHANG k ON dp.MaKH = k.MaKH
                ORDER BY hd.NgayLapHoaDon DESC
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            return results, None
    except Exception as e:
        return None, str(e)
    finally:
        if conn:
            conn.close()
