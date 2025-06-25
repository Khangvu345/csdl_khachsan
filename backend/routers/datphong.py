from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import date
from schemas import datphong as datphong_schema
from crud import datphong as datphong_crud

router = APIRouter(
    prefix="/api/datphong",
    tags=["Đặt Phòng"]
)

@router.post("/",
             response_model=datphong_schema.DatPhongCreate,
             status_code=status.HTTP_201_CREATED,
             summary="Tạo một lượt đặt phòng mới")
def create_datphong(dp: datphong_schema.DatPhongCreate):
    result, error = datphong_crud.create(dp)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

@router.get("/",
                response_model=List[datphong_schema.DatPhongChiTiet], # Sử dụng schema chi tiết mới
                summary="Lấy danh sách đặt phòng có bộ lọc")
def get_all_datphong(
    trang_thai: Optional[str] = Query(None, description="Lọc theo trạng thái: Đã đặt, Đã hủy, Hoàn tất"),
    ngay: Optional[date] = Query(None, description="Lọc theo ngày, định dạng YYYY-MM-DD")
):
    # --- THAY ĐỔI CÁCH GỌI CRUD ĐỂ LẤY DỮ LIỆU MỚI ---
    results, error = datphong_crud.get_all_detailed(trang_thai, ngay) # Gọi hàm mới get_all_detailed
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    return results

@router.put("/{madatphong}", summary="Cập nhật thông tin đặt phòng")
def update_datphong(madatphong: str, dp: datphong_schema.DatPhongUpdate):
    """
    Cập nhật chi tiết của một lượt đặt phòng (ví dụ: ngày nhận/trả).
    """
    result, error = datphong_crud.update(madatphong, dp)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

@router.put("/{madatphong}/cancel",
            summary="Hủy một lượt đặt phòng")
def cancel_datphong(madatphong: str):
    result, error = datphong_crud.cancel(madatphong)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result
