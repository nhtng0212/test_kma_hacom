import pytest
import re
from playwright.sync_api import Page, expect
from pages.home_page import HomePage

# Cấu trúc dữ liệu mẫu cho Data-Driven Testing
SEARCH_DATA = [
    # (Mã kịch bản, Từ khóa nhập vào, Trạng thái hợp lệ)
    ("TC_S01", "Bàn phím cơ", True),
    ("TC_S02", "asdkjasdhkjasd", False),
    ("TC_S03", "", False),
    ("TC_S04", "@#$%^&*", False),
    ("TC_S05", "  lApTop GaMing  ", True),
    ("TC_S07", "logitech", True),
    ("TC_S10", "MELO0142", True),
    ("TC_S11", "ban phim co", True),
    ("TC_S12", "SELECT * FROM items", False),
]


@pytest.mark.parametrize("tc_id, keyword, is_valid", SEARCH_DATA)
def test_search_data_driven(page: Page, tc_id, keyword, is_valid):
    home = HomePage(page)
    print(f"\n🟢 [{tc_id}] Đang test từ khóa: '{keyword}'...")

    home.load()
    home.search_product(keyword)

    if is_valid:
        # Kiểm tra URL đích chứa đường dẫn tìm kiếm tổng quát
        expect(page).to_have_url(re.compile(r".*/tim\?q=.*"), timeout=5000)
        # Kiểm tra ô nhập liệu hiển thị đúng giá trị đã cắt khoảng trắng thừa
        expect(home.search_input).to_have_value(keyword.strip())
        print(f"✅ [{tc_id}] PASSED: Đã chuyển hướng và giữ đúng từ khóa trên UI.")
    else:
        if keyword == "":
            expect(page).not_to_have_url(re.compile(r"q="), timeout=5000)
            print(f"✅ [{tc_id}] PASSED: Bỏ trống không làm chuyển trang.")
        else:
            # Xử lý logic HOẶC trực quan bằng phương thức .or_() của Playwright Python
            locator_h3 = page.locator("h3:has-text('Không có kết quả phù hợp')")
            locator_text = page.locator("text='0 sản phẩm'")
            empty_msg = locator_h3.or_(locator_text).first

            expect(empty_msg).to_be_visible(timeout=8000)
            print(f"✅ [{tc_id}] PASSED: Web chặn an toàn, hiện thông báo không có SP.")


def test_search_auto_suggest(page: Page):
    home = HomePage(page)
    print("\n🟢 [TC_S13] Gõ chữ 'chuột' và đứng đợi Popup gợi ý...")

    home.load()
    home.type_keyword_only("chuột")

    # Kiểm tra sự hiển thị của menu gợi ý động thả xuống
    expect(home.suggest_popup).to_be_visible(timeout=8000)
    expect(home.suggest_items.first).to_be_visible()
    count = home.suggest_items.count()
    print(
        f"✅ [TC_S13] PASSED: Tính năng gợi ý hoạt động tốt, hiển thị {count} sản phẩm."
    )


def test_search_by_click_icon(page: Page):
    home = HomePage(page)
    print("\n🟢 [TC_S14] Nhập từ khóa 'Màn hình' và CLICK KÍNH LÚP...")

    home.load()
    home.type_keyword_only("Màn hình")
    home.click_search_icon()

    expect(page).to_have_url(re.compile(r".*/tim\?q=.*"), timeout=5000)
    print("✅ [TC_S14] PASSED: Nút kính lúp hoạt động tốt!")
