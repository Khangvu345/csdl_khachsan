from pydantic import BaseModel

# --- Schema cho bảng DICHVU ---
class DichVu(BaseModel):
    """Mô hình đại diện cho một Dịch vụ trong CSDL."""
    MaDV: str
    TenDV: str
    GiaDV: float

    class Config:
        from_attributes = True

# --- Schemas cho việc gán dịch vụ (bảng CHI_TIET_DICH_VU) ---

class ChiTietDichVuCreate(BaseModel):
    """Mô hình dữ liệu đầu vào khi gán một dịch vụ cho đặt phòng."""
    MaDatPhong: str
    MaDV: str

class DichVuDaGan(DichVu):
    """
    Mô hình dữ liệu trả về khi xem danh sách dịch vụ đã gán.
    Kế thừa từ DichVu để có đầy đủ thông tin (Tên, Giá).
    """
    pass
