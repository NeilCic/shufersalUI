from datetime import date, timedelta

from pathlib import Path
import json
import pytest

from pages.shufersal.ShufersalDeliveryDetailsPage import ShufersalDeliveryDetailsPage
from pages.shufersal.home_page import ShufersalHomePage
from playwright.async_api import expect

from pages.shufersal.login_page import ShufersalLoginPage
from pages.shufersal.shopping_page import ShufersalSearchResultsPage

DATA_PATH = Path(__file__).parent / "data" / "product_data.json"
with open(DATA_PATH, encoding="utf-8") as f:
    products_data = json.load(f)

valid_products = products_data["valid_product_info"]
invalid_products = products_data["invalid_product_info"]


@pytest.mark.asyncio
@pytest.mark.parametrize("product", valid_products)
async def test_valid_product_search(page_with_device, product) -> None:
    # happy flow test - combines all 3 steps of search, add product to cart and checkout flow
    # I know some companies would rather have 3 separate tests, so it came down to personal preference
    page, is_mobile = page_with_device
    year, month, day = str(date.today() + timedelta(days=1)).split('-')

    home = ShufersalHomePage(page)
    search_results_page = ShufersalSearchResultsPage(page)
    delivery_page = ShufersalDeliveryDetailsPage(page)
    login_page = ShufersalLoginPage(page)

    await home.goto()
    await home.header.search(product['name'])

    product_card = await search_results_page.get_product_card(**product, is_mobile=is_mobile)
    price = await product_card.get_price()
    await product_card.add_to_cart()

    delivery_details = {
        'year': year,
        'month': month,
        'day': day,
        'hour': "20:00",
        'city': "תל אביב - יפו",
        'street': "דיזנגוף",
        'num': "1"
    }
    await delivery_page.fill_in_details(**delivery_details)

    await expect(search_results_page.shopping_cart.cart_counter).to_have_text("1")
    product_names = await search_results_page.shopping_cart.get_cart_products()
    assert len(product_names) == 1
    assert product_names[0]['title'] == product['name']
    assert product_names[0]['price'] == price
    assert product_names[0]['quantity'] == 1
    if is_mobile:
        await home.header.open_cart_mobile()
    await search_results_page.shopping_cart.pay_for_cart()
    await login_page.wait_for_page()
