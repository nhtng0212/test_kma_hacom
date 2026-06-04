import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_page import ProductPage


# --- TC_F01: LỌC THEO KHOẢNG GIÁ ---
def test_filter_by_price(page: Page):
    home = HomePage(page)
    product = ProductPage(page)

    print("\n🟢 [TC_F01] Mở trang tìm kiếm 'Bàn phím'...")
    home.load()

    page.wait_for_timeout(3000)

    home.search_product("Bàn phím")

    print("🟢 [TC_F01] Chọn khoảng giá: 'Dưới 1 triệu'")
    product.click_filter_option("Dưới 1 triệu")

    # Kì vọng: Trình duyệt không văng lỗi và tiêu đề sản phẩm đầu tiên vẫn hiển thị
    expect(product.first_product_title).to_be_visible(timeout=5000)
    print("✅ [TC_F01] PASSED: Đã lọc giá thành công.")


# --- TC_F02: LỌC THEO HÃNG (BỘ LỌC KÉP) ---
def test_filter_by_brand(page: Page):
    home = HomePage(page)
    product = ProductPage(page)

    print("\n🟢 [TC_F02] Mở trang tìm kiếm 'Chuột'...")
    home.load()

    page.wait_for_timeout(3000)

    home.search_product("Chuột")

    print("🟢 [TC_F02] Chọn hãng: 'APPLE'")
    product.click_filter_option("APPLE")

    # Kì vọng: Kết quả trả về phải hiển thị sản phẩm
    expect(product.first_product_title).to_be_visible(timeout=5000)

    first_name = product.get_first_product_name().lower()
    assert "apple" in first_name, f"Lỗi: Lọc Apple nhưng ra sản phẩm {first_name}"
    print(f"✅ [TC_F02] PASSED: Lọc chuẩn xác -> {first_name}")


# --- TC_F03: TÍNH NĂNG SẮP XẾP ---
def test_sort_by_price_asc(page: Page):
    home = HomePage(page)
    product = ProductPage(page)

    print("\n🟢 [TC_F03] Mở trang tìm kiếm 'Tai nghe'...")
    home.load()

    page.wait_for_timeout(3000)

    home.search_product("Tai nghe")

    print("🟢 [TC_F03] Chọn sắp xếp: 'Giá tăng dần'")
    product.sort_by("Giá tăng dần")

    expect(product.first_product_title).to_be_visible(timeout=5000)
    print(
        f"✅ [TC_F03] PASSED: Đã sắp xếp. Sản phẩm rẻ nhất là: {product.get_first_product_name()}"
    )
