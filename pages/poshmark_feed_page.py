from playwright.sync_api import Page, expect
import re

class poshmarkFeed:

    def __init__(self,page: Page):
        self.page = page

        #locators
        self.feed_sold_tag = page.locator(".icon.tile__inventory-tag.sold-tag")
        self.feed_search_title = page.locator(".search__title").filter(has_text="Search results for : ")
        self.feed_new_listing_tag = page.get_by_text("New Listings")
        self.feed_unit = page.locator(".feed__unit")
        self.feed_image = page.locator(".feed__unit__content .img__container img")
        self.feed_like_button = page.locator(".icon.heart-black-empty")
        self.feed_unlike_button = page.locator(".icon.liked")
        self.price_all_prices = page.locator('label[data-test="checkbox-label"]', has_text="All Prices")
        self.price_under_25 = page.locator('label[data-test="checkbox-label"]', has_text="Under $25")
        self.price_25_to_50 = page.locator('label[data-test="checkbox-label"]', has_text="$25 - $50")
        self.price_50_to_100 = page.locator('label[data-test="checkbox-label"]', has_text="$50 - $100")
        self.price_100_to_250 = page.locator('label[data-test="checkbox-label"]', has_text="$100 - $250")
        self.price_250_to_500 = page.locator('label[data-test="checkbox-label"]', has_text="$250 - $500")
        self.price_over_500 = page.locator('label[data-test="checkbox-label"]', has_text="Over $500")



    def get_all_items_price(self) -> list[float]:
        price_elements = self.page.locator("span.p--t--1.fw--bold").all_inner_texts()

        cleaned_price = []
        for text in price_elements:
            if not "$" in text  :
                continue
            cleaned_price.append(float(text.replace("$", "").replace(",", "").strip()))
        
        return cleaned_price


    
    def make_filter_visible(self, category: str):
        
        header = self.page.locator('.toggle__header', has_text=re.compile(category, re.IGNORECASE))
        
        current_classes = header.get_attribute("class") or ""
        
        if "show" not in current_classes:
            header.click()
            # Wait for the animation to expand the options below it
            self.page.wait_for_selector('.toggle__header.show', state="visible")

    def click_filter(self, category: str, option: str):

        target  = None
    
        try:
            # BRAND FILTER
            if category == "Brand":
                self.page.get_by_placeholder("Search brands...").fill(option)
                target = self.page.locator(".form__group--check.textbox-list-selector__item").get_by_text(option, exact=True)
    
  
            # PRICE, SIZE, SHIPPING, CONDITION, AND AVAILABILITY FILTERS
            elif category == "Price" or category == "Size" or category == "Shipping" or category == "Condition" or category == "Availability":
                target = self.page.locator('.form__group--check.form_list-item').get_by_text(option, exact=True)
    
            # COLOR FILTER
            elif category == "Color":
                target = self.page.locator(f'[data-et-prop-content="{option}"]')
    
            else:
                raise ValueError(f"Filter category '{category}' not recognized. Use 'brand', 'size', 'price', 'shipping', 'condition', 'availability', or 'color'.")
            

            #Smart filter checking

            current_classes = target.get_attribute("class") or ""

            if not category == "Color" or category == "Brand": #color and brand filters behave differently than the rest, so we handle them separately
                if "fw--med" not in current_classes: #if filter is NOT checked, move to it and wait for click
                    pass

                else:  #else if filter is already checked, we uncheck it first before reapplying
                    target.click(delay=1000, force=True)
                    self.page.wait_for_timeout(500)
            elif category == "Color":
                checkmark_icon = target.locator('i.checkmark')
                
                if checkmark_icon.count() == 0: #if color is not checked, move to it and wait for click
                    pass
                else:
                    target.click(delay = 500, force=True) #uncheck the color filter first before reapplying
                    self.page.wait_for_timeout(1000)
            elif category == "Brand":

                all_brands = self.page.locator(".form__group--check.textbox-list-selector__item").get_by_text(re.compile(r"All Brands", re.IGNORECASE), exact=True)
                
                #If the target brand filter is not checked, we move to it and wait for click,
                if  "fw--med" not in current_classes: 
                    pass

                #but if it's already checked, we click "All Brands" to uncheck it first before reapplying the filter
                else: 
                    self.page.wait_for_timeout(500)
                    all_brands.click(delay=500, force=True)  

            else:
                print("Unexpected filter category. No action taken.")    

            self.page.wait_for_timeout(500)
            target.click(delay=500, force=True)
          


    
        except Exception as e:
            raise Exception(f"Failed to apply filter '{option}' for category '{category}'. Error: {e}")

        
    
    def return_filter(self,text_name: str):
        return self.page.get_by_label(text_name)
    
    def force_like_first_listing(self):

        first_lisiting = self.feed_unit.first
        first_like_button = self.feed_like_button.first
        first_unlike_button = self.feed_unlike_button.first
        first_lisiting.scroll_into_view_if_needed()
        #clicking like button can sometimes fail if the listing is already liked, 
        # so we check for that and unlike first if needed before liking
        if not first_like_button.is_visible(timeout=3000):	
            first_unlike_button.click()
            self.page.wait_for_timeout(2000)
            first_like_button.click()			
        else:
            first_like_button.click()