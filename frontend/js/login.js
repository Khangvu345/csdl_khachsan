document.addEventListener('DOMContentLoaded', () => {

    // Lấy các phần tử từ DOM
    const loginForm = document.getElementById('auth-form');
    const errorMessageElement = document.getElementById('error-message');

    // Bắt sự kiện khi người dùng nhấn nút "Đăng Nhập"
    loginForm.addEventListener('submit', async (event) => {
        // Ngăn chặn hành vi mặc định của form (tải lại trang)
        event.preventDefault();

        // Xóa thông báo lỗi cũ
        errorMessageElement.textContent = '';

        // Lấy dữ liệu từ form
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Tạo đối tượng dữ liệu để gửi đi
        const formData = {
            TenDangNhap: username,
            MatKhau: password
        };

        try {
            // Gửi yêu cầu POST đến API backend bằng fetch
            const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            // Lấy dữ liệu JSON từ phản hồi
            const result = await response.json();

            // Nếu phản hồi không thành công (status code không phải 2xx)
            if (!response.ok) {
                // Ném ra một lỗi với thông điệp từ server
                throw new Error(result.detail || 'Đã có lỗi xảy ra.');
            }

            // Nếu đăng nhập thành công
            alert('Đăng nhập thành công!');
            // Chuyển hướng người dùng đến trang dashboard (bạn cần tạo file này)
            window.location.href = 'dashboard.html';

        } catch (error) {
            // Hiển thị thông báo lỗi lên giao diện
            errorMessageElement.textContent = error.message;
        }
    });
});