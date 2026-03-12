from playwright.sync_api import Page, expect
import pytest
from pages.poshmark_feed_page import poshmarkFeed

pytestmark = pytest.mark.regression

def test_search_bar(page : Page, base_url: str, search_item: str, filter_category: str, filter_option: str):
	search_page=poshmarkFeed(page)

	page.goto(base_url)
	search_page.item_search(search_item)
	search_page.apply_filter(filter_category, filter_option)

	expect(search_page.search_title).to_contain_text("Search results for : ")

	expect(search_page.return_filter(filter_category)).to_be_visible()
	expect(search_page.sold_tag).to_have_count(0)