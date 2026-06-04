import pytest
import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


@pytest.mark.parametrize(
    "test_id, keyword, expected_scenario",
    [
        ("TC_S01", "Bàn phím cơ", "valid"),
        ("TC_S02", "asdkjasdhkjasd", "not_found"),  # Từ khóa không tồn tại
        ("TC_S03", "", "empty"),  # Bỏ trống từ khóa
        ("TC_S04", "@#$%^&*", "not_found"),  # Ký tự đặc biệt
    ],
)
def test_search_multiple_scenarios(page: Page, test_id, keyword, expected_scenario):
    home_page = HomePage(page)

    print(f"\n🟢 [{test_id}]: Đang mở trang chủ...")
    home_page.load()

    print(f"🟢 [{test_id}]: Gõ từ khóa '{keyword}' và ấn Enter...")
    home_page.search_product(keyword)

    print(f"🟢 [{test_id}]: Kiểm tra kết quả hiển thị...")

    # KỊCH BẢN 1: TÌM KIẾM HỢP LỆ
    if expected_scenario == "valid":
        # Kì vọng 1: URL phải chuyển sang trang tìm kiếm
        expect(page).to_have_url(re.compile(r"(q=|search)"))
        print(f"✅ [{test_id}] PASSED: Đã ra kết quả hợp lệ.")

    # KỊCH BẢN 2 & 4: KHÔNG TÌM THẤY SẢN PHẨM
    elif expected_scenario == "not_found":
        # Kì vọng 1: URL vẫn chuyển sang trang tìm kiếm
        expect(page).to_have_url(re.compile(r"(q=|search)"))

        # Kì vọng 2: Trang web phải hiện dòng thông báo ""
        empty_msg = page.locator("h3", has_text="Không có kết quả phù hợp").first
        expect(empty_msg).to_be_visible(timeout=5000)
        print(f"✅ [{test_id}] PASSED: Đã chặn từ khóa rác thành công.")

    # KỊCH BẢN 3: BỎ TRỐNG
    elif expected_scenario == "empty":
        # Khi bỏ trống và ấn Enter, trang web thường không làm gì cả (giữ nguyên URL)
        expect(page).not_to_have_url(re.compile(r"q="))
        print(f"✅ [{test_id}] PASSED: Đã xử lý đúng case bỏ trống tìm kiếm.")
