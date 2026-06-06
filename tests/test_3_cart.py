import pytest
import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

# =====================================================================
# MODULE 3: KIỂM THỬ CHỨC NĂNG GIỎ HÀNG (8 Test Cases)
# =====================================================================


def test_TC_C04_add_item_to_cart(page: Page):
    home, product, cart = HomePage(page), ProductPage(page), CartPage(page)
    print("\n🟢 [TC_C04] Thêm sản phẩm vào giỏ hàng: Tìm 'Màn hình' và thêm vào giỏ")

    home.load()
    home.search_product("Màn hình")

    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
        product.go_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()
        product.go_to_cart()

    # Kì vọng: Ô hiển thị tổng tiền xuất hiện, chứng tỏ giỏ hàng có đồ
    expect(cart.total_price).to_be_visible(timeout=8000)
    print("✅ [TC_C04] PASSED: Sản phẩm đã xuất hiện trong giỏ hàng thành công.")


def test_TC_C01_increase_quantity_updates_price(page: Page):
    home, product, cart = HomePage(page), ProductPage(page), CartPage(page)
    print("\n🟢 [TC_C01] Tăng số lượng sản phẩm: Thêm chuột vào giỏ và bấm (+)")

    home.load()
    home.search_product("Chuột Logitech")
    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
        product.go_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()
        product.go_to_cart()

    initial_price = cart.get_total_price()

    cart.increase_quantity(1)
    page.wait_for_timeout(1500)  # Đợi API load giá mới

    # Kì vọng: Giá tiền phải nhảy số khác giá ban đầu
    expect(cart.total_price).not_to_have_text(initial_price, timeout=5000)
    print(
        f"✅ [TC_C01] PASSED: Giá đã cập nhật thành công từ {initial_price} sang {cart.get_total_price()}."
    )


def test_TC_C02_decrease_quantity_at_minimum(page: Page):
    home, product, cart = HomePage(page), ProductPage(page), CartPage(page)
    print(
        "\n🟢 [TC_C02] Giảm số lượng ở mức tối thiểu: Đang ở số lượng 1, bấm nút giảm (-)"
    )

    home.load()
    home.search_product("Chuột Logitech")
    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
        product.go_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()
        product.go_to_cart()

    qty_input = page.locator("div[role='group'] input[type='text']").first

    cart.decrease_quantity(1)
    page.wait_for_timeout(1000)

    # Kì vọng: Ô input vẫn phải là "1" (không được tụt về 0)
    expect(qty_input).to_have_value("1")
    print("✅ [TC_C02] PASSED: Web đã chặn thành công, không cho số lượng tụt xuống 0.")


def test_TC_C03_delete_item_from_cart(page: Page):
    home, product, cart = HomePage(page), ProductPage(page), CartPage(page)
    print("\n🟢 [TC_C03] Xóa sản phẩm: Thêm bàn phím vào giỏ và bấm nút Xóa")

    home.load()
    home.search_product("Bàn phím cơ")
    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
        product.go_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()
        product.go_to_cart()

    cart.delete_item()

    # Kì vọng: Dòng chữ thông báo giỏ hàng trống phải hiện ra
    expect(cart.empty_cart_msg).to_be_visible(timeout=5000)
    print("✅ [TC_C03] PASSED: Đã xóa sản phẩm và hiện thông báo giỏ hàng trống.")


def test_TC_C05_add_same_item_multiple_times(page: Page):
    home, product, cart = HomePage(page), ProductPage(page), CartPage(page)
    print(
        "\n🟢 [TC_C05] Thêm cùng một sản phẩm nhiều lần: Thêm 1 loại chuột 2 lần liên tiếp"
    )

    home.load()
    home.search_product("Chuột Logitech")
    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()

    # Bấm thêm vào giỏ 2 lần liên tiếp
    page.wait_for_timeout(1000)
    product.add_first_item_to_cart()

    product.go_to_cart()

    qty_input = page.locator("div[role='group'] input[type='text']").first

    # Kì vọng: Số lượng trong input box phải là 2 (tăng số lượng, không đẻ ra 2 dòng)
    expect(qty_input).to_have_value("2")
    print("✅ [TC_C05] PASSED: Hệ thống tự động gộp dòng và cộng dồn số lượng.")


def test_TC_C06_refresh_page_keeps_cart_data(page: Page):
    home, product, cart = HomePage(page), ProductPage(page), CartPage(page)
    print("\n🟢 [TC_C06] Refresh trang: Thêm đồ vào giỏ và F5 trình duyệt")

    home.load()
    home.search_product("Laptop Acer")
    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
        product.go_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()
        product.go_to_cart()

    initial_price = cart.get_total_price()

    # F5 làm mới trình duyệt
    page.reload()
    page.wait_for_load_state("domcontentloaded")

    # Kì vọng: Tổng tiền vẫn phải y nguyên như trước khi F5
    expect(cart.total_price).to_have_text(initial_price, timeout=5000)
    print(
        "✅ [TC_C06] PASSED: Dữ liệu giỏ hàng được bảo toàn hoàn hảo sau khi Refresh."
    )


def test_TC_C07_calculate_total_price(page: Page):
    home, product, cart = HomePage(page), ProductPage(page), CartPage(page)
    print("\n🟢 [TC_C07] Kiểm tra toán học: Tổng tiền = Đơn giá x Số lượng")

    home.load()
    home.search_product("Bàn phím")
    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
        product.go_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()
        product.go_to_cart()

    # Lấy giá của 1 sản phẩm trước khi tăng (Chỉ lấy các chữ số)
    unit_price_str = re.sub(r"[^\d]", "", cart.get_total_price())
    unit_price = int(unit_price_str) if unit_price_str else 0

    # Tăng thêm 2 sản phẩm (Tổng là 3)
    cart.increase_quantity(2)
    page.wait_for_timeout(2000)

    # Lấy tổng tiền sau khi tăng
    total_price_str = re.sub(r"[^\d]", "", cart.get_total_price())
    total_price = int(total_price_str) if total_price_str else 0

    # Kì vọng: Tổng = Đơn giá x 3
    assert total_price == (
        unit_price * 3
    ), f"Sai logic tính toán: {unit_price} * 3 != {total_price}"
    print(
        f"✅ [TC_C07] PASSED: Hệ thống tính toán chính xác ({unit_price}đ x 3 = {total_price}đ)."
    )


def test_TC_C08_clear_all_items_in_cart(page: Page):
    home, product, cart = HomePage(page), ProductPage(page), CartPage(page)
    print(
        "\n🟢 [TC_C08] Xóa toàn bộ sản phẩm: Thêm nhiều loại sản phẩm và ấn nút Xóa tất cả"
    )

    # Thêm sản phẩm 1
    home.load()
    home.search_product("Chuột Logitech")
    page.wait_for_timeout(3000)
    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
        product.go_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()
        product.go_to_cart()

    # Thêm sản phẩm 2
    home.search_product("Bàn phím cơ")
    product.select_sort("Đánh giá")
    page.wait_for_timeout(3000)

    try:
        product.add_first_item_to_cart()
        product.go_to_cart()
    except:
        product.select_sort("Giá tăng dần")
        page.wait_for_timeout(3000)
        product.add_first_item_to_cart()
        product.go_to_cart()

    # Click trực tiếp nút Xóa toàn bộ thay vì dùng vòng lặp while
    print("   [-] Đang bấm nút Xóa toàn bộ...")
    cart.clear_all_items()

    # Kì vọng: Trống trơn
    expect(cart.empty_cart_msg).to_be_visible(timeout=15000)
    print("✅ [TC_C08] PASSED: Đã xóa sạch giỏ hàng bằng nút Xóa toàn bộ thành công.")
