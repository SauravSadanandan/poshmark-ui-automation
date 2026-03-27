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
    ("Sneakers", "Color", "Red"),
    ("T-Shirt", "Color", "White"),
    ("Dress", "Color", "Black"),
    ("Nike", "Color", "Gold"),
])

def test_color_filter(setup_poshmark, page: Page, search_item: str, filter_category: str, filter_option: str):
    
    feed_page, header_page = setup_poshmark
    
    #search for item
    header_page.item_search(search_item)
    #make filter visible and click
    feed_page.make_filter_visible(filter_category)
    feed_page.click_filter(filter_category, filter_option)

    #Wait for the fiter to apply
    expect(page).to_have_url(re.compile(r"color", re.IGNORECASE), timeout=5000)    
    expect(page.locator(".tile-shimmer").first).to_be_hidden()

    first_card = page.locator(".card.card--small.tile").first
    expect(first_card).to_be_visible()

    selected_color = page.locator(f'[data-et-prop-content="{filter_option}"]').locator("i.checkmark").first
    selected_color.scroll_into_view_if_needed()
    expect(selected_color).to_be_visible()
    