from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import khachhang as khachhang_schema
from crud import khachhang as khachhang_crud

router = APIRouter(
    prefix="/api/khachhang",
    tags=["Khách Hàng"]
)

@router.post("/",
             response_model=khachhang_schema.KhachHangCreate,
             status_code=status.HTTP_201_CREATED,
             summary="Tạo một khách hàng mới")
def create_khachhang(kh: khachhang_schema.KhachHangCreate):
    result, error = khachhang_crud.create(kh)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

@router.get("/",
            response_model=List[khachhang_schema.KhachHang],
            summary="Lấy danh sách tất cả khách hàng")
def get_all_khachhang():
    result, error = khachhang_crud.get_all()
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    return result

@router.put("/{makh}", summary="Cập nhật thông tin khách hàng")
def update_khachhang(makh: str, kh: khachhang_schema.KhachHangUpdate):
    result, error = khachhang_crud.update(makh, kh)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

@router.delete("/{makh}", summary="Xóa một khách hàng")
def delete_khachhang(makh: str):
    """
    Xóa một khách hàng khỏi CSDL.
    Frontend sẽ chịu trách nhiệm hiển thị hộp thoại xác nhận trước khi gọi API này.
    """
    result, error = khachhang_crud.delete(makh)
    if error:
        # Trả về lỗi 400 nếu không thể xóa (ví dụ: có ràng buộc khóa ngoại)
        # hoặc 404 nếu không tìm thấy.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Đừng quên thêm router này vào file app/main.py của bạn:
# from .routers import khachhang
# app.include_router(khachhang.router)