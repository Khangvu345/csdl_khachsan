from pydantic import BaseModel
from datetime import date
from typing import Optional

# --- Schema cho dữ liệu gửi lên khi tạo hóa đơn (giữ nguyên) ---
class HoaDonCreateRequest(BaseModel):
    MaHoaDon: str
    PhuongThucThanhToan: str
    MaNV: str
    MaDatPhong: str

# --- Schema cơ bản của một hóa đơn (giữ nguyên) ---
class HoaDon(BaseModel):
    MaHoaDon: str
    NgayLapHoaDon: date
    TongTienHoaDon: float
    PhuongThucThanhToan: str
    MaNV: str
    MaDatPhong: str

    class Config:
        from_attributes = True

# --- THÊM SCHEMA MỚI: Dùng để hiển thị danh sách chi tiết ---
class HoaDonChiTiet(HoaDon):
    """
    Schema để hiển thị thông tin chi tiết của hóa đơn,
    kèm theo thông tin từ các bảng liên quan.
    """
    TenKhachHang: Optional[str] = None
    TenNhanVien: Optional[str] = None
    MaPhong: Optional[str] = None