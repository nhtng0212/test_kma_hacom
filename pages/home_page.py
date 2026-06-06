from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        # Định vị ô input tìm kiếm hiển thị trên màn hình (bỏ qua bản mobile ẩn)
        self.search_input = page.locator("input[name='search']:visible").first
        # Định vị icon kính lúp hiển thị trên desktop
        self.search_icon = page.locator(".fa-magnifying-glass:visible").first
        # Định vị tiêu đề khối sản phẩm đề xuất trong popup gợi ý
        self.suggest_popup = page.locator("h3:has-text('Sản phẩm đề xuất')").first
        # Danh sách các link sản phẩm con nằm trong khối popup gợi ý
        self.suggest_items = self.suggest_popup.locator("xpath=..").locator("a")

    def load(self):
        self.page.goto("https://hacom.vn/")
        self.page.wait_for_load_state("domcontentloaded")

        self.close_ads()

    def close_ads(self):
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

        fallback_btn = (
            self.page.locator("button")
            .filter(has=self.page.locator("span.sr-only:has-text('Close')"))
            .first
        )

        if fallback_btn.is_visible(timeout=1500):
            # print(
            #     "   [!] Phím ESC không tác dụng, dùng Locator tắt Banner quảng cáo..."
            # )
            fallback_btn.click(force=True)
            self.page.wait_for_timeout(500)

    def search_product(self, keyword: str):
        self.search_input.fill(keyword)
        self.search_input.press("Enter")
        self.page.wait_for_timeout(2000)

    def type_keyword_only(self, keyword: str):
        self.search_input.fill(keyword)
        self.page.wait_for_timeout(2000)

    def click_search_icon(self):
        self.search_icon.click(force=True)
        self.page.wait_for_timeout(2000)
