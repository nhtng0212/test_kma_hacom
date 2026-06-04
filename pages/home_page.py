from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page

        self.search_box = page.locator("input[name='search']:visible").first

        self.close_popup_btn = page.locator(
            "//*[@id='ins-frameless-overlay']//*[contains(@class, 'ins-close-button')]"
        )

    def load(self):
        self.page.goto(
            "https://hacom.vn/", wait_until="domcontentloaded", timeout=60000
        )
        self.page.wait_for_timeout(5000)
        if self.close_popup_btn.is_visible():
            self.close_popup_btn.click()
            print("\n[Log] Đã đóng popup quảng cáo.")

    def search_product(self, keyword: str):
        self.search_box.fill(keyword)
        print(f"\n[Log] Đã gõ: {keyword}")
        self.search_box.press("Enter")
        print("[Log] Đã bấm Enter.")


# pytest tests/ -v -s --headed --html=report.html
