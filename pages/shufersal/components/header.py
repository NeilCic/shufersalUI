import allure


class Header:
    def __init__(self, page):
        self.page = page
        self.search_input = page.locator("#js-site-search-input")
        self.cart_mobile = page.locator("li.mobileTop.openCart.hidden-lg-header")
        # Potentially we could add here מבצעים, סופרמרקט etc, but not needed for assignment. I'm trying to keep this to the point.

    @allure.step("Search for product {val}")
    async def search(self, val: str):
        await self.search_input.fill(val)
        await self.search_input.press("Enter")

    async def open_cart_mobile(self):
        await self.cart_mobile.click()
