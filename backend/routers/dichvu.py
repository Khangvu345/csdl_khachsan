from fastapi import APIRouter, HTTPException, status, Body
from typing import List
from schemas import dichvu as dichvu_schema
from crud import dichvu as dichvu_crud

router = APIRouter(
    tags=["Dịch Vụ Đặt Phòng"]  # Tên nhóm trong Swagger UI
)


@router.post("/api/datphong/{madatphong}/dichvu",
             response_model=dichvu_schema.ChiTietDichVuCreate,
             status_code=status.HTTP_201_CREATED,
             summary="Gán một dịch vụ cho một lượt đặt phòng")
def assign_service_to_booking(madatphong: str, MaDV: str = Body(..., embed=True, description="Mã dịch vụ cần gán")):
    """
    Tạo một bản ghi trong bảng CHI_TIET_DICH_VU.
    - **madatphong**: Lấy từ URL path.
    - **MaDV**: Lấy từ request body.
    """
    # Tạo object schema từ các tham số đã nhận
    detail_to_create = dichvu_schema.ChiTietDichVuCreate(MaDatPhong=madatphong, MaDV=MaDV)

    result, error = dichvu_crud.assign_service(detail_to_create)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


@router.get("/api/datphong/{madatphong}/dichvu",
            response_model=List[dichvu_schema.DichVuDaGan],
            summary="Xem danh sách dịch vụ đã gán cho một lượt đặt phòng")
def get_assigned_services(madatphong: str):
    """
    Trả về một danh sách các dịch vụ với đầy đủ thông tin (Tên, Giá)
    đã được gán cho `madatphong` được cung cấp.
    """
    result, error = dichvu_crud.get_services_by_booking_id(madatphong)
    if error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error)
    return result