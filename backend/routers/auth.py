from fastapi import APIRouter, HTTPException, status
from schemas import taikhoan as taikhoan_schema
from crud import taikhoan as taikhoan_crud

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/login", summary="Xác thực đăng nhập người dùng")
def login(form_data: taikhoan_schema.TaiKhoanLogin):
    """
    Xác thực người dùng và trả về token nếu thành công.
    """
    # Gọi hàm crud từ file crud/taikhoan.py
    taikhoan_db = taikhoan_crud.get_by_username(form_data.TenDangNhap)

    # Kiểm tra xác thực
    if not taikhoan_db or taikhoan_db["MatKhau"] != form_data.MatKhau:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng",
        )

    # Nếu thành công
    return {"message": "Đăng nhập thành công! Đang chuyển hướng..."}
