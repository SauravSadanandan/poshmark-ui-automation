from playwright.sync_api import Page, expect
from pages.poshmark_search_page import PoshmarkSearchPage

def test_poshmark_search(page : Page, base_url: str):
	search_page=PoshmarkSearchPage(page)

	page.goto(base_url)
	search_page.item_search("Nike shoes")
	search_page.apply_filter("availability", "Available Items")

	expect(search_page.search_title).to_have_text("Search results for : ")

	expect(search_page.return_filter("availability")).to_be_visible()
	expect(search_page.sold_tag).to_have_count(0)