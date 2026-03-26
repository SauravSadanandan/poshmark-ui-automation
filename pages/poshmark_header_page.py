from playwright.sync_api import Page, expect


class poshmarkHeader:

	def __init__(self,page: Page):
		self.page = page

		#locators
		self.header_search_bar = page.get_by_placeholder("Search Listings")

	def item_search(self,item_name: str):
		self.header_search_bar.fill(item_name)
		self.header_search_bar.press("Enter")