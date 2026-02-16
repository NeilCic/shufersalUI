import pytest
from playwright.async_api import async_playwright, Page
import allure


@pytest.fixture(params=[
    ("chromium", "desktop"),
    ("chromium", "mobile"),
    ("firefox", "desktop"),
    ("msedge", "desktop"),
])
async def page_with_device(request) -> Page:
    browser_name, device_type = request.param
    headless = not request.config.getoption("--headed")

    async with async_playwright() as p:
        try:
            if browser_name == "chromium":
                browser = await p.chromium.launch(headless=headless)

            elif browser_name == "firefox":
                browser = await p.firefox.launch(headless=headless)
            elif browser_name == "msedge":
                browser = await p.chromium.launch(channel="msedge", headless=headless)
            else:
                raise ValueError(f"Unknown browser: {browser_name}")
        except Exception:
            pytest.skip(f"{browser_name} cannot be launched")

        if device_type == "mobile":
            pixel_4 = p.devices["Pixel 4"]
            context = await browser.new_context(**pixel_4)
        else:
            context = await browser.new_context()

        page = await context.new_page()
        page.set_default_timeout(60000)
        yield page, device_type == 'mobile'

        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            screenshot = await page.screenshot()
            allure.attach(
                screenshot,
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

        await context.close()
        await browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
