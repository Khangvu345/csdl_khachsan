from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, khachhang, datphong, dichvu, hoadon

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Hotel Management API",
    description="API để quản lý các hoạt động của khách sạn.",
    version="1.0.0"
)

# Cấu hình CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- BAO GỒM CÁC ROUTERS ---
app.include_router(auth.router)
app.include_router(khachhang.router)
app.include_router(datphong.router)
app.include_router(dichvu.router)
app.include_router(hoadon.router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint gốc để kiểm tra xem API có hoạt động hay không.
    """
    return {"message": "Chào mừng đến với API Quản lý Khách sạn!"}