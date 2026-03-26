from playwright.sync_api import Page, expect


class poshmarkListing:

	def __init__(self,page: Page):
		self.page = page
		
	    #locators
	
		self.listing_sold_msg = page.get_by_text("THIS ITEM IS SOLD!")
		self.listing_image = page.locator(".img__container picture img")
		self.listing_buy_now_button = page.get_by_role("button", name="Buy Now")
