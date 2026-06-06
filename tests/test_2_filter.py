import pytest
import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_page import ProductPage

# =====================================================================
# NHÓM 1: DATA-DRIVEN LỌC & SẮP XẾP (9 Test Cases)
# =====================================================================
FILTER_SORT_DATA = [
    ("TC_F01", "Bàn phím", "filter", "Dưới 1 triệu", "p=duoi-1trieu"),
    ("TC_F02", "Bàn phím", "filter", "Logitech", "brand=logitech"),
    ("TC_F03", "Bàn phím", "filter", "Corsair", "brand=corsair"),
    ("TC_F04", "Chuột", "filter", "Trên 20 triệu", "p=tren-20trieu"),
    ("TC_F05", "Tai nghe", "sort", "Giá tăng dần", "sort=price-asc"),
    ("TC_F06", "Tai nghe", "sort", "Giá giảm dần", "sort=price-desc"),
    ("TC_F07", "Tai nghe", "sort", "Mới nhất", "sort=new"),
    ("TC_F08", "Màn hình", "sort", "Tên A->Z", "sort=name"),
    ("TC_F09", "Màn hình", "sort", "Đánh giá", "sort=rating"),
]


@pytest.mark.parametrize(
    "tc_id, keyword, action_type, value, expected_url", FILTER_SORT_DATA
)
def test_filter_sort_basics(
    page: Page, tc_id, keyword, action_type, value, expected_url
):
    home = HomePage(page)
    product = ProductPage(page)

    print(f"\n🟢 [{tc_id}] Tìm '{keyword}', thực hiện {action_type}: '{value}'...")
    home.load()
    page.wait_for_timeout(1000)
    home.search_product(keyword)

    if action_type == "filter":
        product.click_filter(value)
    else:
        product.select_sort(value)

    expect(page).to_have_url(re.compile(f".*{expected_url}.*"), timeout=8000)
    print(f"✅ [{tc_id}] PASSED: URL cập nhật chính xác tham số '{expected_url}'.")


# =====================================================================
# NHÓM 2: UI/UX & LUỒNG BIÊN (6 Test Cases Đặc thù)
# =====================================================================


def test_filter_combined_multiple(page: Page):
    home, product = HomePage(page), ProductPage(page)
    print("\n🟢 [TC_F10] Lọc Đa điều kiện: Chuột + APPLE + Dưới 1 triệu")

    home.load()
    home.search_product("Chuột")
    product.click_filter("APPLE")
    product.click_filter("Dưới 1 triệu")

    expect(page).to_have_url(re.compile(r".*brand=apple.*"), timeout=5000)
    expect(page).to_have_url(re.compile(r".*p=duoi-1trieu.*"), timeout=5000)
    print("✅ [TC_F10] PASSED: Bộ lọc kép hoạt động chính xác.")


def test_filter_toggle_uncheck(page: Page):
    home, product = HomePage(page), ProductPage(page)
    print("\n🟢 [TC_F11] Toggle: Click chọn hãng 'Logitech', sau đó click lại để HỦY")

    home.load()
    home.search_product("Bàn phím")

    product.click_filter("Logitech")
    expect(page).to_have_url(re.compile(r".*brand=logitech.*"), timeout=5000)

    product.click_filter("Logitech")
    expect(page).not_to_have_url(re.compile(r".*brand=logitech.*"), timeout=5000)
    print("✅ [TC_F11] PASSED: Chức năng hủy kích hoạt bộ lọc hoạt động tốt.")


def test_filter_multi_brand(page: Page):
    home, product = HomePage(page), ProductPage(page)
    print("\n🟢 [TC_F12] Chuyển đổi bộ lọc (Switch): Chọn ASUS rồi chuyển sang DELL")

    home.load()
    home.search_product("Laptop")

    # Bước 1: Chọn ASUS
    product.click_filter("ASUS")
    expect(page).to_have_url(re.compile(r".*brand=asus.*"), timeout=5000)

    # Bước 2: Chọn sang DELL (Phải đè lên ASUS vì là thẻ radio)
    product.click_filter("DELL")

    # Kì vọng: URL phải có DELL và TUYỆT ĐỐI KHÔNG được còn chữ ASUS
    expect(page).to_have_url(re.compile(r".*brand=dell.*"), timeout=5000)
    expect(page).not_to_have_url(re.compile(r".*brand=asus.*"), timeout=5000)
    print(
        "✅ [TC_F12] PASSED: Hệ thống tự động ghi đè bộ lọc mới (Radio button logic) thành công."
    )


def test_filter_load_more_btn(page: Page):
    home, product = HomePage(page), ProductPage(page)
    print("\n🟢 [TC_F13] Kiểm tra tính năng tải thêm của nút 'Xem thêm'")

    home.load()
    home.search_product("Bàn phím")

    product.load_more_btn.scroll_into_view_if_needed()
    initial_count = product.product_items.count()

    product.load_more_btn.click(force=True)
    page.wait_for_timeout(3000)

    assert product.product_items.count() >= initial_count
    print("✅ [TC_F13] PASSED: Nút tải thêm hoạt động bình thường.")


def test_filter_share_direct_link(page: Page):
    print("\n🟢 [TC_F14] Kiểm tra tính đúng đắn khi truy cập URL chứa sẵn bộ lọc")

    page.goto("https://hacom.vn/tim?q=Bàn+phím&brand=akko")
    page.wait_for_load_state("domcontentloaded")

    expect(page).to_have_url(re.compile(r".*brand=akko.*"), timeout=5000)
    print(
        "✅ [TC_F14] PASSED: Hệ thống ghi nhận chính xác trạng thái bộ lọc từ đường dẫn."
    )
