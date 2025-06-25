from pydantic import BaseModel

class TaiKhoanLogin(BaseModel):
    """
    Schema cho dữ liệu form đăng nhập.
    """
    TenDangNhap: str
    MatKhau: str
