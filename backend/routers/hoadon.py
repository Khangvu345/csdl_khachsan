from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import hoadon as hoadon_schema
from crud import hoadon as hoadon_crud

router = APIRouter(
    prefix="/api/hoadon",
    tags=["Hóa Đơn"]
)

# --- THÊM ENDPOINT MỚI ---
@router.get("/",
            response_model=List[hoadon_schema.HoaDonChiTiet],
            summary="Lấy danh sách tất cả hóa đơn")
def get_all_invoices():
    """
    Trả về danh sách tất cả hóa đơn đã được tạo, kèm theo thông tin chi tiết.
    """
    result, error = hoadon_crud.get_all()
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    return result

# --- Endpoint tạo hóa đơn (giữ nguyên) ---
@router.post("/",
             response_model=hoadon_schema.HoaDon,
             status_code=status.HTTP_201_CREATED,
             summary="Tạo hóa đơn mới, tính tiền và hoàn tất đặt phòng")
def create_new_invoice(request_data: hoadon_schema.HoaDonCreateRequest):
    result, error = hoadon_crud.create_invoice(request_data)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result
