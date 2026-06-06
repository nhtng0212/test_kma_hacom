from playwright.sync_api import Page
import re


class CartPage:
    def __init__(self, page: Page):
        self.page = page

        self.increase_btn = (
            page.locator("div[role='group'] button:visible").filter(has_text="+").first
        )
        self.decrease_btn = (
            page.locator("div[role='group'] button:visible").filter(has_text="−").first
        )

        self.delete_btn = page.locator("button:has(svg:has(path[d^='M8.75 1']))").first

        self.total_price = page.locator("span:has-text('Cần thanh toán') + span").first

        # self.delete_btn = page.locator(
        #     "button[title*='Xóa'], button:has(svg.fa-trash-alt), a:has-text('Xóa')"
        # ).first

        self.empty_cart_msg = page.locator(
            "p:has-text('Chưa có sản phẩm nào trong giỏ hàng')"
        ).first

        self.clear_all_btn = page.locator(
            "button:has(svg:has(path[d^='M8.75 1'])).bg-default.w-8.h-8"
        ).first

    def decrease_quantity(self, times: int = 1):
        self.page.wait_for_timeout(2000)
        for _ in range(times):
            self.decrease_btn.click()

    def delete_item(self):
        self.page.wait_for_timeout(2000)

        self.delete_btn.click(force=True)

        self.page.wait_for_timeout(1000)

        confirm_btn = self.page.locator("button").filter(has_text="Xóa").last
        confirm_btn.click(force=True)

        self.page.wait_for_timeout(2000)

    def increase_quantity(self, times: int = 1):
        self.page.wait_for_timeout(2000)

        for _ in range(times):
            self.increase_btn.click(force=True)

    def get_total_price(self) -> str:
        self.total_price.wait_for(state="visible")
        return self.total_price.text_content().strip()

    def get_quantity(self) -> int:
        # Lấy giá trị từ ô input textbox số lượng
        qty_str = self.page.locator(
            "div[role='group'] input[type='text']"
        ).first.input_value()
        return int(qty_str)

    def extract_price_number(self, price_text: str) -> int:
        clean_text = re.sub(r"[^\d]", "", price_text)
        return int(clean_text) if clean_text else 0

    def get_item_unit_price(self) -> int:
        # Lấy đơn giá của 1 sản phẩm (thường nằm cạnh tên sản phẩm hoặc có class chứa giá)
        # Chú ý: Cần soi lại DOM thực tế chỗ hiển thị đơn giá gốc để bắt cho chuẩn
        unit_price_element = self.page.locator(
            ".cart-item-info span:has-text('đ'), .item-price span"
        ).first
        price_text = unit_price_element.text_content().strip()
        return self.extract_price_number(price_text)

    def clear_all_items(self):
        self.page.wait_for_timeout(2000)
        self.clear_all_btn.click(force=True)

        # Nếu hệ thống có popup hỏi "Bạn có chắc chắn muốn xóa toàn bộ?", thêm dòng xác nhận ở đây
        confirm_btn = self.page.locator("button").filter(has_text="Xóa").last
        if confirm_btn.is_visible():
            confirm_btn.click(force=True)

        self.page.wait_for_timeout(2000)
