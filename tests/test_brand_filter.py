import re
import pytest
from playwright.sync_api import Page, expect
from pages.poshmark_feed_page import poshmarkFeed
from pages.poshmark_header_page import poshmarkHeader

pytestmark = pytest.mark.regression

@pytest.fixture
def setup_poshmark(page: Page, base_url: str):
    page.goto(base_url, wait_until="domcontentloaded")
    return poshmarkFeed(page), poshmarkHeader(page)


@pytest.mark.parametrize("search_item, filter_category, filter_option", [
    ("Sneakers", "Brand", "Nike"),
    ("T-Shirt", "Brand", "Puma"),
    ("Dress", "Brand", "adidas"),
    ("Nike", "Brand", "Calvin Klein"),
])
def test_brand_filter(setup_poshmark, page: Page, search_item: str, filter_category: str, filter_option: str):
    feed_page, header_page = setup_poshmark
    
    # 1. Search for item
    header_page.item_search(search_item)
    
    # 2. Make filter visible and click
    feed_page.make_filter_visible(filter_category)
    feed_page.click_filter(filter_category, filter_option)

    # 3. Wait for the filter to apply (Network & UI stabilization)
    expect(page).to_have_url(re.compile(r"brand", re.IGNORECASE), timeout=5000)    
    expect(page.locator(".tile-shimmer").first).to_be_hidden()

    # 4. Verify feed is not empty
    first_card = page.locator(".card.card--small.tile").first
    expect(first_card).to_be_visible()

    # 5. Verify the item details actually contain the applied brand name
    details_locator = first_card.locator(".item__details")
    expect(details_locator).to_contain_text(re.compile(filter_option, re.IGNORECASE))
