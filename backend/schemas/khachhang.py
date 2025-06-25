from pydantic import BaseModel, EmailStr
from typing import Optional, List

class KhachHangBase(BaseModel):
    """Schema cơ bản, chứa các trường chung."""
    Ho: str
    Ten: str
    TenDem: Optional[str] = None
    Email: Optional[EmailStr] = None
    DiaChi: str

class KhachHangCreate(KhachHangBase):
    """
    Schema dùng khi tạo mới một khách hàng.
    Yêu cầu phải có MaKH và ít nhất một số điện thoại.
    """
    MaKH: str
    SDT: str

class KhachHangUpdate(BaseModel):
    """
    Schema dùng khi cập nhật thông tin khách hàng.
    Tất cả các trường đều là tùy chọn.
    """
    Ho: Optional[str] = None
    TenDem: Optional[str] = None
    Ten: Optional[str] = None

    Email: Optional[EmailStr] = None
    DiaChi: Optional[str] = None
    SDT: Optional[str] = None # Cho phép cập nhật SĐT chính

class KhachHang(KhachHangBase):
    """
    Schema dùng để hiển thị thông tin khách hàng ra ngoài API.
    Kế thừa từ Base và thêm các trường không có trong Base.
    """
    MaKH: str
    # Một khách hàng có thể có nhiều SĐT, nên sẽ hiển thị dưới dạng danh sách
    SDT: List[str] = []

    class Config:
        # Cho phép Pydantic đọc dữ liệu từ các đối tượng ORM/database
        from_attributes = True
