import pytest

from pages.shufersal.home_page import ShufersalHomePage


@pytest.mark.asyncio
async def test_page_load_times(page_with_device, product_name: str = "milk", time_limit_ms=30_000) -> None:
    page, is_mobile = page_with_device

    async def assert_page_load_time(p):
        await p.wait_for_load_state('load')
        load_time = await p.evaluate("""() => {
                const t = performance.timing;
                return t.loadEventEnd - t.navigationStart;
            }""")
        assert load_time < time_limit_ms, f"Page load too slow: {load_time}ms"

    home = ShufersalHomePage(page)
    await home.goto()
    await assert_page_load_time(page)

    await home.header.search(product_name)
    await assert_page_load_time(page)
