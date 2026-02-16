import allure
from playwright.async_api import expect


class ShufersalDeliveryDetailsPage:
    def __init__(self, page):
        self.page = page
        self.city_input_bar = page.locator("input#cityInput")
        self.street_name_bar = page.locator("input#streetInput")
        self.street_num_bar = page.get_by_role("textbox", name="מספר")
        self.continue_button = page.get_by_role("button", name="להמשך")
        self.date_options = page.locator("div.slick-track")
        self.save_button = page.get_by_role("button", name="שמירה")

    async def fill_in_city(self, city):
        await expect(self.city_input_bar).to_be_visible(timeout=60000)
        await expect(self.city_input_bar).to_be_enabled()
        await self.city_input_bar.click()
        await self.city_input_bar.fill(city)
        await self.page.get_by_text(city).click()

    async def fill_in_street_details(self, street, num):
        await self.street_name_bar.fill(street)
        await self.page.get_by_text(street, exact=True).click()
        await self.street_num_bar.fill(num)
        await self.continue_button.click()

    async def fill_in_date(self, year, month, day, hour):
        time_options = self.date_options.locator(f"div#day_{year}{month}{day}").locator('..')
        await time_options.locator(f"label[aria-label*='{hour}']").click()
        await self.save_button.click()

    @allure.step("Fill in delivery details")
    async def fill_in_details(self, year, month, day, hour="20:00", city="תל אביב - יפו", street="דיזנגוף", num="1"):
        await self.fill_in_city(city)
        await self.fill_in_street_details(street, num)
        await self.fill_in_date(year, month, day, hour)

