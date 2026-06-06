import re
from playwright.sync_api import Page


class ProductPage:
    def __init__(self, page: Page):
        self.page = page

        # Định vị thông báo trống khi bộ lọc không có sản phẩm phù hợp
        self.empty_msg = (
            page.locator("h3:has-text('Không có kết quả phù hợp')")
            .or_(page.locator("text='0 sản phẩm'"))
            .first
        )

        # Nút Xem thêm kết quả ở dưới cùng danh sách sản phẩm
        self.load_more_btn = page.locator("button:has(span:has-text('Xem thêm'))").first

        # Danh sách tiêu đề của các sản phẩm hiển thị trên màn hình
        self.product_items = page.locator("h3.line-clamp-2")

        #
        self.filter_asus = page.locator("input[id='brand-asus']").first

        self.first_product_title = page.locator("h3.line-clamp-2").first

        self.add_to_cart_btn = page.locator("button:has(i.fa-cart-shopping)").first

        self.cart_icon = page.locator("a[href='/gio-hang']:visible").first

    def click_filter(self, filter_text: str):
        print(f"\n[LOG] Bắt đầu tìm filter: {filter_text}")

        # =====================================================
        # FILTER GIÁ
        # =====================================================
        price_mapping = {
            "Dưới 1 triệu": "duoi-1trieu",
            "1 triệu - 4 triệu": "1trieu-4trieu",
            "4 triệu - 10 triệu": "4trieu-10trieu",
            "10 triệu - 20 triệu": "10trieu-20trieu",
            "Trên 20 triệu": "tren-20trieu",
        }

        if filter_text in price_mapping:
            target_label = self.page.locator(
                f"label[for='price-{price_mapping[filter_text]}']:not(.sr-only)"
            ).first

            target_label.wait_for(state="visible", timeout=5000)
            target_label.scroll_into_view_if_needed()
            target_label.click(delay=50)

            print(f"[LOG] Đã tick chọn giá: {filter_text}")
            self.page.wait_for_timeout(2500)
            return

        brand = filter_text.lower().strip()

        target_label = self.page.locator(
            f"label[for='brand-{brand}']:not(.sr-only)"
        ).first

        # Nút xem thêm hãng
        show_more_btn = (
            self.page.locator("button:not(.btn-megamenu):visible")
            .filter(has_text="Xem thêm")
            .filter(has_text="hãng")
            .first
        )

        # Mở rộng danh sách hãng nếu cần
        for i in range(20):
            if target_label.is_visible():
                print(f"[LOG] Hãng '{filter_text}' đã hiển thị trên màn hình.")
                break

            if show_more_btn.is_visible():
                print(
                    f"[LOG] Lần {i+1}: Hãng chưa xuất hiện. Đang bấm tải thêm 5 hãng..."
                )

                show_more_btn.scroll_into_view_if_needed()
                show_more_btn.click(delay=50)
                self.page.wait_for_timeout(1000)
            else:
                print(
                    "[LOG] Không tìm thấy nút Xem thêm nữa (Danh sách đã mở hết hoặc đang bị ẩn)."
                )
                break

        target_label.wait_for(state="visible", timeout=5000)
        target_label.scroll_into_view_if_needed()
        target_label.click(delay=50)

        print(f"[LOG] Đã tick chọn thành công hãng: {filter_text}")

        self.page.wait_for_timeout(2500)

    def select_sort(self, sort_text: str):
        # Sử dụng ID tĩnh của bản Desktop để chọn điều kiện sắp xếp ổn định 100%
        sort_dropdown = self.page.locator("#desktop-sort-select")
        sort_dropdown.select_option(label=sort_text)
        self.page.wait_for_timeout(2500)

    def add_first_item_to_cart(self):
        self.first_product_title.hover()
        self.add_to_cart_btn.click(force=True)

        self.page.wait_for_timeout(2000)

        self.page.keyboard.press("Escape")
        print("\n[Log] Đã đóng popup bằng phím ESC.")

        self.page.wait_for_timeout(3000)

    def go_to_cart(self):
        self.cart_icon.click(force=True)
        self.page.wait_for_load_state("domcontentloaded")

    def get_first_product_name(self) -> str:
        return self.first_product_title.text_content().strip()
