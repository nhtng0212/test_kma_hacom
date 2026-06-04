from playwright.sync_api import Page


class ProductPage:
    def __init__(self, page: Page):
        self.page = page

        self.filter_asus = page.locator("input[id='brand-asus']").first

        self.first_product_title = page.locator("h3.line-clamp-2").first

        self.add_to_cart_btn = page.locator("button:has(i.fa-cart-shopping)").first

        self.cart_icon = page.locator("a[href='/gio-hang']:visible").first

    def filter_by_asus(self):
        self.filter_asus.check(force=True)
        self.page.wait_for_timeout(2000)

    def get_first_product_name(self) -> str:
        return self.first_product_title.text_content().strip()

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

    def click_filter_option(self, option_text: str):
        target_label = (
            self.page.locator("label.cursor-pointer").filter(has_text=option_text).first
        )

        target_label.evaluate("node => node.click()")

        self.page.wait_for_timeout(3000)

    def sort_by(self, label_text: str):
        self.page.locator("select#desktop-sort-select").select_option(label=label_text)
        self.page.wait_for_timeout(2000)
