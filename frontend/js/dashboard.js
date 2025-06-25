// File: frontend/js/dashboard.js (Bản cập nhật đầy đủ)

document.addEventListener('DOMContentLoaded', () => {
    // === KHAI BÁO BIẾN ===
    const navLinks = document.querySelectorAll('.nav-link');
    const contentSections = document.querySelectorAll('.content-section');
    const modal = document.getElementById('form-modal');
    const closeModalBtn = document.querySelector('.close-btn');
    const modalForm = document.getElementById('modal-form');
    const modalTitle = document.getElementById('modal-title');
    const apiBaseUrl = 'http://127.0.0.1:8000/api';

    const btnLogout = document.getElementById('logout-btn');

    let currentFormMode = 'add_customer';
    let currentEditId = null;

    // === XỬ LÝ CHUNG ===
    const openModal = () => modal.style.display = 'flex';
    const closeModal = () => {
        modal.style.display = 'none';
        modalForm.reset();
        modalForm.innerHTML = '';
    };
    closeModalBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // SỬA ĐỔI: Thêm logic tải hóa đơn khi chuyển tab
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-target');
            navLinks.forEach(nav => nav.classList.remove('active'));
            contentSections.forEach(section => section.classList.remove('active'));
            link.classList.add('active');
            document.getElementById(targetId).classList.add('active');

            // Tải dữ liệu tương ứng khi chuyển tab
            if (targetId === 'khachhang-section') loadKhachHang();
            if (targetId === 'datphong-section') loadDatPhong();
            if (targetId === 'hoadon-section') loadHoaDon(); // <--- Thêm dòng này
        });
    });

    if (btnLogout) {
        btnLogout.addEventListener('click', () => {
            if (confirm("Bạn có chắc muốn đăng xuất không?")) {
                window.location.href = 'index.html';
            }
        });
    }

    // === QUẢN LÝ KHÁCH HÀNG (Giữ nguyên) ===
    const khachHangTableBody = document.getElementById('khachhang-table-body');
    const btnAddKhachHang = document.getElementById('btn-add-khachhang');
    async function loadKhachHang() {
        try {
            const response = await fetch(`${apiBaseUrl}/khachhang/`);
            if (!response.ok) throw new Error('Không thể tải dữ liệu khách hàng');
            const data = await response.json();
            khachHangTableBody.innerHTML = '';
            data.forEach(kh => {
                const row = `
                    <tr>
                        <td>${kh.MaKH}</td>
                        <td>${kh.Ho} ${kh.TenDem || ''} ${kh.Ten}</td>
                        <td>${kh.Email || ''}</td>
                        <td>${kh.DiaChi || ''}</td>
                        <td>${kh.SDT ? kh.SDT.join(', ') : ''}</td>
                        <td>
                            <button class="action-btn btn-edit" onclick="editKhachHang('${kh.MaKH}')">Sửa</button>
                            <button class="action-btn btn-delete" onclick="deleteKhachHang('${kh.MaKH}')">Xóa</button>
                        </td>
                    </tr>
                `;
                khachHangTableBody.innerHTML += row;
            });
        } catch (error) {
            alert(error.message);
        }
    }
    btnAddKhachHang.addEventListener('click', () => {
        currentFormMode = 'add_customer';
        modalTitle.textContent = "Thêm Khách Hàng Mới";
        modalForm.innerHTML = `
            <div class="input-group"><label>Mã KH (*)</label><input type="text" name="MaKH" required></div>
            <div class="input-group"><label>Họ (*)</label><input type="text" name="Ho" required></div>
            <div class="input-group"><label>Tên Đệm</label><input type="text" name="TenDem"></div>
            <div class="input-group"><label>Tên (*)</label><input type="text" name="Ten" required></div>
            <div class="input-group"><label>Email</label><input type="email" name="Email"></div>
            <div class="input-group"><label>Địa Chỉ (*)</label><input type="text" name="DiaChi" required></div>
            <div class="input-group"><label>Số Điện Thoại (*)</label><input type="text" name="SDT" required></div>
            <button type="submit" class="btn-primary">Lưu</button>
        `;
        openModal();
    });
    window.editKhachHang = async (maKH) => {
        const response = await fetch(`${apiBaseUrl}/khachhang/`);
        const khachhangs = await response.json();
        const kh = khachhangs.find(k => k.MaKH === maKH);
        if (!kh) return alert('Không tìm thấy khách hàng!');
        currentFormMode = 'edit_customer';
        currentEditId = maKH;
        modalTitle.textContent = `Cập Nhật TT Khách Hàng: ${maKH}`;
        modalForm.innerHTML = `
            <div class="input-group"><label>Họ (*)</label><input type="text" name="Ho" value="${kh.Ho}" required></div>
            <div class="input-group"><label>Tên Đệm</label><input type="text" name="TenDem" value="${kh.TenDem || ''}"></div>
            <div class="input-group"><label>Tên (*)</label><input type="text" name="Ten" value="${kh.Ten}" required></div>
            <div class="input-group"><label>Email</label><input type="email" name="Email" value="${kh.Email || ''}"></div>
            <div class="input-group"><label>Địa Chỉ (*)</label><input type="text" name="DiaChi" value="${kh.DiaChi || ''}" required></div>
            <div class="input-group"><label>Số Điện Thoại (*)</label><input type="text" name="SDT" value="${kh.SDT ? kh.SDT.join(', ') : ''}" required></div>
            <button type="submit" class="btn-primary">Cập Nhật</button>
        `;
        openModal();
    };
    window.deleteKhachHang = async (maKH) => {
        if (!confirm(`Bạn có chắc chắn muốn xóa khách hàng ${maKH}?`)) return;
        try {
            const response = await fetch(`${apiBaseUrl}/khachhang/${maKH}`, { method: 'DELETE' });
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail);
            }
            alert('Xóa khách hàng thành công!');
            loadKhachHang();
        } catch (error) {
            alert('Lỗi: ' + error.message);
        }
    };

    // === QUẢN LÝ ĐẶT PHÒNG (Giữ nguyên) ===
    const datPhongTableBody = document.getElementById('datphong-table-body');
    const btnAddDatPhong = document.getElementById('btn-add-datphong');
    const btnFilterDatPhong = document.getElementById('btn-filter-datphong');
    async function loadDatPhong() {
        const trangThai = document.getElementById('filter-trangthai').value;
        const ngay = document.getElementById('filter-ngay').value;
        let url = new URL(`${apiBaseUrl}/datphong/`);
        if (trangThai) url.searchParams.append('trang_thai', trangThai);
        if (ngay) url.searchParams.append('ngay', ngay);
        try {
            const response = await fetch(url);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Lỗi từ server: ${JSON.stringify(errorData.detail)}`);
            }
            const data = await response.json();
            datPhongTableBody.innerHTML = '';
            data.forEach(dp => {
                const row = `
                    <tr>
                        <td>${dp.MaDatPhong}</td>
                        <td>${dp.TenKhachHang} (KH: ${dp.MaKH})</td>
                        <td>${dp.TenPhong} (P: ${dp.MaPhong})</td>
                        <td>${dp.NgayNhanPhong}</td>
                        <td>${dp.NgayTraPhong}</td>
                        <td><span class="status-${dp.TrangThaiDatPhong.replace(' ', '-').toLowerCase()}">${dp.TrangThaiDatPhong}</span></td>
                        <td>
                            ${dp.TrangThaiDatPhong === 'Đã đặt' ? `
                                <button class="action-btn btn-edit" onclick="editDatPhong('${dp.MaDatPhong}', '${dp.NgayNhanPhong}', '${dp.NgayTraPhong}')">Sửa</button>
                                <button class="action-btn btn-service" onclick="ganDichVu('${dp.MaDatPhong}')">Gán DV</button>
                                <button class="action-btn btn-invoice" onclick="lapHoaDon('${dp.MaDatPhong}')">Lập HĐ</button>
                                <button class="action-btn btn-cancel" onclick="cancelDatPhong('${dp.MaDatPhong}')">Hủy</button>
                            ` : ''}
                        </td>
                    </tr>
                `;
                datPhongTableBody.innerHTML += row;
            });
        } catch (error) {
            alert(error.message);
        }
    }
    btnAddDatPhong.addEventListener('click', () => {
        currentFormMode = 'add_booking';
        modalTitle.textContent = "Tạo Đặt Phòng Mới";
        modalForm.innerHTML = `
            <div class="input-group"><label>Mã Đặt Phòng (*)</label><input type="text" name="MaDatPhong" required></div>
            <div class="input-group"><label>Mã Khách Hàng (*)</label><input type="text" name="MaKH" required></div>
            <div class="input-group"><label>Mã Phòng (*)</label><input type="text" name="MaPhong" required></div>
            <div class="input-group"><label>Ngày Nhận (*)</label><input type="date" name="NgayNhanPhong" required></div>
            <div class="input-group"><label>Ngày Trả (*)</label><input type="date" name="NgayTraPhong" required></div>
            <button type="submit" class="btn-primary">Tạo Đặt Phòng</button>
        `;
        openModal();
    });
    window.editDatPhong = (maDatPhong, ngayNhan, ngayTra) => {
        currentFormMode = 'edit_booking';
        currentEditId = maDatPhong;
        modalTitle.textContent = `Cập Nhật Đặt Phòng: ${maDatPhong}`;
        modalForm.innerHTML = `
            <div class="input-group"><label>Ngày Nhận (*)</label><input type="date" name="NgayNhanPhong" value="${ngayNhan}" required></div>
            <div class="input-group"><label>Ngày Trả (*)</label><input type="date" name="NgayTraPhong" value="${ngayTra}" required></div>
            <button type="submit" class="btn-primary">Cập Nhật</button>
        `;
        openModal();
    };
    window.cancelDatPhong = async (maDatPhong) => {
        if (!confirm(`Bạn chắc chắn muốn hủy đặt phòng ${maDatPhong}?`)) return;
        try {
            const response = await fetch(`${apiBaseUrl}/datphong/${maDatPhong}/cancel`, { method: 'PUT' });
            if (!response.ok) { const err = await response.json(); throw new Error(err.detail); }
            alert('Hủy đặt phòng thành công!');
            loadDatPhong();
        } catch (error) { alert('Lỗi: ' + error.message); }
    }
    window.ganDichVu = async (maDatPhong) => {
        const maDV = prompt(`Nhập mã dịch vụ muốn gán cho đặt phòng ${maDatPhong}:`);
        if (!maDV) return;
        try {
            const response = await fetch(`${apiBaseUrl}/datphong/${maDatPhong}/dichvu`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ MaDV: maDV })
            });
            if (!response.ok) { const err = await response.json(); throw new Error(err.detail); }
            alert(`Gán dịch vụ ${maDV} cho ${maDatPhong} thành công!`);
        } catch(error) {
            alert('Lỗi: ' + error.message);
        }
    };
    window.lapHoaDon = async (maDatPhong) => {
        const maNV = prompt("Nhập mã nhân viên lập hóa đơn (vd: NV01):");
        const maHD = prompt("Nhập mã hóa đơn mới (vd: HD01):");
        const pttt = prompt("Nhập phương thức thanh toán (vd: Tiền mặt):");
        if (!maNV || !maHD || !pttt) return alert("Vui lòng nhập đủ thông tin.");

        if (!confirm(`Xác nhận lập hóa đơn cho đặt phòng ${maDatPhong}?`)) return;
        try {
            const response = await fetch(`${apiBaseUrl}/hoadon`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ MaHoaDon: maHD, PhuongThucThanhToan: pttt, MaNV: maNV, MaDatPhong: maDatPhong })
            });
            if (!response.ok) { const err = await response.json(); throw new Error(err.detail); }
            alert('Lập hóa đơn và hoàn tất đặt phòng thành công!');
            loadDatPhong();
        } catch(error) {
            alert('Lỗi: ' + error.message);
        }
    };
    btnFilterDatPhong.addEventListener('click', loadDatPhong);

    // +++ THÊM LOGIC MỚI CHO QUẢN LÝ HÓA ĐƠN +++
    const hoaDonTableBody = document.getElementById('hoadon-table-body');
    async function loadHoaDon() {
        try {
            const response = await fetch(`${apiBaseUrl}/hoadon/`);
            if (!response.ok) throw new Error('Không thể tải dữ liệu hóa đơn');
            const data = await response.json();

            hoaDonTableBody.innerHTML = '';
            data.forEach(hd => {
                const row = `
                    <tr>
                        <td>${hd.MaHoaDon}</td>
                        <td>${hd.TenKhachHang}</td>
                        <td>${hd.MaPhong}</td>
                        <td>${hd.NgayLapHoaDon}</td>
                        <td>${new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(hd.TongTienHoaDon)}</td>
                        <td>${hd.PhuongThucThanhToan}</td>
                        <td>${hd.TenNhanVien} (${hd.MaNV})</td>
                    </tr>
                `;
                hoaDonTableBody.innerHTML += row;
            });
        } catch (error) {
            alert(error.message);
        }
    }

    // === XỬ LÝ SUBMIT FORM TRUNG TÂM (Giữ nguyên) ===
    modalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(modalForm);
        let data = Object.fromEntries(formData.entries());
        let url = '';
        let method = 'POST';
        let successMessage = '';
        let body = {};
        if (currentFormMode === 'add_customer') {
            url = `${apiBaseUrl}/khachhang/`;
            successMessage = 'Thêm khách hàng thành công!';
            body = data;
        } else if (currentFormMode === 'edit_customer') {
            url = `${apiBaseUrl}/khachhang/${currentEditId}`;
            method = 'PUT';
            successMessage = 'Cập nhật khách hàng thành công!';
            body = data;
        } else if (currentFormMode === 'add_booking') {
            url = `${apiBaseUrl}/datphong/`;
            successMessage = 'Tạo đặt phòng thành công!';
            body = data;
        } else if (currentFormMode === 'edit_booking') {
            url = `${apiBaseUrl}/datphong/${currentEditId}`;
            method = 'PUT';
            successMessage = 'Cập nhật đặt phòng thành công!';
            body = {
                NgayNhanPhong: data.NgayNhanPhong,
                NgayTraPhong: data.NgayTraPhong
            };
        }
        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.detail);
            alert(successMessage);
            closeModal();
            if (currentFormMode.includes('customer')) loadKhachHang();
            if (currentFormMode.includes('booking')) loadDatPhong();
        } catch (error) {
            alert('Lỗi: ' + error.message);
        }
    });

    // === KHỞI TẠO ===
    loadKhachHang();
});