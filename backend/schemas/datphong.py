from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import date

# --- Lớp cơ sở ---
class DatPhongBase(BaseModel):
    """Schema cơ sở chứa các thông tin cốt lõi của một lượt đặt phòng."""
    MaDatPhong: str
    NgayNhanPhong: date
    NgayTraPhong: date
    MaKH: str
    MaPhong: str
    TrangThaiDatPhong: str

# --- SỬA LỖI: Đưa lớp DatPhong lên trước khi được sử dụng ---
class DatPhong(DatPhongBase):
    """Schema dùng để hiển thị hoặc trả về thông tin đặt phòng đầy đủ."""
    pass

    class Config:
        # Cho phép Pydantic đọc dữ liệu từ các thuộc tính của object (ORM mode)
        from_attributes = True


# --- Các lớp kế thừa hoặc sử dụng cho mục đích cụ thể ---
class DatPhongCreate(DatPhongBase):
    """
    Schema sử dụng khi tạo một lượt đặt phòng mới.
    Trạng thái mặc định sẽ là 'Đã đặt'.
    """
    TrangThaiDatPhong: str = "Đã đặt"

    # Validator để đảm bảo ngày trả phải sau hoặc bằng ngày nhận
    @model_validator(mode='after')
    def check_dates(self) -> 'DatPhongCreate':
        if self.NgayNhanPhong and self.NgayTraPhong:
            if self.NgayTraPhong < self.NgayNhanPhong:
                raise ValueError('Ngày trả phòng phải sau hoặc trùng với ngày nhận phòng.')
        return self

class DatPhongChiTiet(DatPhong):
    """
    Schema để hiển thị thông tin chi tiết của một lượt đặt phòng
    kèm theo Tên Phòng và Tên Khách Hàng.
    """
    TenPhong: Optional[str] = None
    TenKhachHang: Optional[str] = None

class DatPhongUpdate(BaseModel):
    """Schema sử dụng riêng cho việc cập nhật ngày nhận/trả phòng."""
    NgayNhanPhong: date
    NgayTraPhong: date