from playwright.sync_api import Page


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
            "text='Chưa có sản phẩm nào trong giỏ hàng'"
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
