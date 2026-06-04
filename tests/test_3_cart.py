import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


# --- TC_C01: TĂNG SỐ LƯỢNG VÀ KIỂM TRA TIỀN ---
def test_increase_quantity_updates_price(page: Page):
    home = HomePage(page)
    product = ProductPage(page)
    cart = CartPage(page)

    print("\n🟢 [TC_C01] Thêm chuột vào giỏ...")
    home.load()
    home.search_product("Chuột Logitech")
    product.add_first_item_to_cart()
    product.go_to_cart()

    initial_price = cart.get_total_price()
    print("🟢 [TC_C01] Bấm nút tăng số lượng (+)...")
    cart.increase_quantity(1)

    # Kì vọng: Giá tiền phải nhảy số khác giá ban đầu
    expect(cart.total_price).not_to_have_text(initial_price, timeout=10000)
    print(
        f"✅ [TC_C01] PASSED: Giá đã cập nhật thành công từ {initial_price} sang {cart.get_total_price()}"
    )


# --- TC_C02: LUỒNG BIÊN - BẤM GIẢM KHI SỐ LƯỢNG LÀ 1 ---
def test_decrease_quantity_at_minimum(page: Page):
    home = HomePage(page)
    product = ProductPage(page)
    cart = CartPage(page)

    print("\n🟢 [TC_C02] Thêm chuột vào giỏ...")
    home.load()
    home.search_product("Chuột Logitech")
    product.add_first_item_to_cart()
    product.go_to_cart()

    # ô textbox chứa số lượng (đang có giá trị là 1)
    qty_input = page.locator("div[role='group'] input[type='text']").first

    print("🟢 [TC_C02] Đang ở số lượng 1, bấm nút giảm (-)...")
    cart.decrease_quantity(1)
    page.wait_for_timeout(2000)

    # Kì vọng: Ô input vẫn phải là "1" (không được tụt về 0)
    expect(qty_input).to_have_value("1")
    print("✅ [TC_C02] PASSED: Web đã chặn thành công, không cho số lượng tụt xuống 0.")


# --- TC_C03: XÓA SẢN PHẨM KHỎI GIỎ ---
def test_delete_item_from_cart(page: Page):
    home = HomePage(page)
    product = ProductPage(page)
    cart = CartPage(page)

    print("\n🟢 [TC_C03] Thêm bàn phím vào giỏ...")
    home.load()
    home.search_product("Bàn phím cơ")
    product.add_first_item_to_cart()
    product.go_to_cart()

    print("🟢 [TC_C03] Bấm nút Xóa sản phẩm...")
    cart.delete_item()

    # Kì vọng: Dòng chữ thông báo giỏ hàng trống phải hiện ra
    expect(cart.empty_cart_msg).to_be_visible(timeout=5000)
    print("✅ [TC_C03] PASSED: Đã xóa sản phẩm và hiện thông báo giỏ hàng trống.")
