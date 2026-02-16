from pages.shufersal.components.header import Header
from pages.shufersal.components.shopping_cart import ShoppingCart


class ShufersalHomePage:
    URL = "https://www.shufersal.co.il/online/"

    def __init__(self, page):
        self.page = page
        self.header = Header(page)
        self.shopping_cart = ShoppingCart(page)

    async def goto(self):
        await self.page.goto(self.URL, wait_until="domcontentloaded", timeout=60_000)
