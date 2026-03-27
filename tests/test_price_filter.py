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


@pytest.mark.parametrize("search_item, filter_category, filter_option, min_price, max_price", [
    ("Shoes", "Price", "Under $25", 0, 25),
    ("Shirt", "Price", "$25 - $50", 25, 50),
    ("Jacket", "Price", "$50 - $100", 50, 100),
    ("Watch", "Price", "Over $500", 500, 999999)
])

def test_price_filter(setup_poshmark, page: Page, search_item: str, filter_category: str, filter_option: str, min_price: int, max_price: int):
    
    feed_page, header_page = setup_poshmark
    
    #search for item
    header_page.item_search(search_item)
    #make filter visible and click
    feed_page.make_filter_visible(filter_category)
    feed_page.click_filter(filter_category, filter_option)

    #Wait for the fiter to apply
    expect(page).to_have_url(re.compile(r"price", re.IGNORECASE), timeout=5000)    
    expect(page.locator(".tile-shimmer").first).to_be_hidden()

    actual_prices = feed_page.get_all_items_price()
    
    #verify page is not empty after filter is applied
    first_card = page.locator(".card.card--small.tile").first
    expect(first_card).to_be_visible()

    #verify all prices are within the selected filter range
    assert all(min_price <= price <= max_price for price in actual_prices), \
        f"Filter failed! Found prices outside the {min_price} to {max_price} range. Actual prices: {actual_prices}"
    
