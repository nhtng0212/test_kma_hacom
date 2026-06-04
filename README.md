# test_kma_hacom
Module 1: Tìm kiếm (Search) - Áp dụng Data-Driven Testing

TC_S01 (Happy Path): Tìm kiếm với từ khóa hợp lệ (Bàn phím cơ).

Kỳ vọng: Chuyển hướng sang trang kết quả có chứa tham số q=.

TC_S02 (Negative): Tìm kiếm với từ khóa không tồn tại (asdkjasdhkjasd).

Kỳ vọng: Hiển thị thông báo "Không có kết quả phù hợp".

TC_S03 (Boundary): Bỏ trống từ khóa và nhấn Enter.

Kỳ vọng: Trình duyệt không chuyển trang (không có tham số q= trên URL).

TC_S04 (Negative): Tìm kiếm với ký tự đặc biệt (@#$%^&*).

Kỳ vọng: Xử lý an toàn, hiển thị thông báo "Không có kết quả phù hợp" (không bị crash web).

Module 2: Lọc & Sắp xếp (Filter & Sort) - Xử lý UI ẩn/phức tạp

TC_F01 (Filter Price): Lọc sản phẩm theo khoảng giá (Dưới 1 triệu).

Kỳ vọng: Trình duyệt cuộn đúng vị trí, click lọc thành công và danh sách sản phẩm được cập nhật.

TC_F02 (Filter Brand): Lọc kết hợp 2 điều kiện (Tìm Chuột -> Lọc hãng APPLE).

Kỳ vọng: Tên sản phẩm trả về đầu tiên phải chứa từ khóa "apple". (Xử lý thành công lỗi thẻ HTML bị ẩn bằng JS Injection).

TC_F03 (Sort): Sắp xếp danh sách sản phẩm (Giá tăng dần).

Kỳ vọng: Thao tác thành công trên dropdown select của giao diện Desktop.

Module 3: Giỏ hàng (Cart) - Xử lý Race Condition & Popup

TC_C01 (Update & Validate): Tăng số lượng sản phẩm lên 2.

Kỳ vọng: Tổng tiền của đơn hàng phải được tính toán và tự động cập nhật khác với giá ban đầu (Smart Wait).

TC_C02 (Boundary): Bấm nút giảm (-) khi số lượng đang ở mức tối thiểu (1).

Kỳ vọng: Hệ thống chặn lại, số lượng trong ô input vẫn giữ nguyên là 1, không bị tụt xuống 0 hay số âm.

TC_C03 (Delete & Modal): Xóa sản phẩm khỏi giỏ hàng.

Kỳ vọng: Tự động bắt và ấn xác nhận (Accept) trên Popup HTML, sau đó hiển thị thông báo "Chưa có sản phẩm nào trong giỏ hàng".
