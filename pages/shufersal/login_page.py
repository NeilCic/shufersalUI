from playwright.async_api import expect

from pages.shufersal.components.header import Header
from pages.shufersal.components.shopping_cart import ShoppingCart


class ShufersalLoginPage:
    URL = "https://www.shufersal.co.il/online/he/login"

    def __init__(self, page):
        self.page = page
        self.header = Header(page)
        self.shopping_cart = ShoppingCart(page)

    async def wait_for_page(self):
        await expect(self.page.locator('#j_username')).to_be_visible()
