import os

import pytest

pytestmark = [
    pytest.mark.skipif(not os.getenv("RUN_E2E"), reason="Set RUN_E2E=1 to run browser sync test"),
    pytest.mark.asyncio,
]


async def test_sync_two_clients(browser_contexts):
    ctx1, ctx2 = browser_contexts
    page1 = await ctx1.new_page()
    page2 = await ctx2.new_page()

    app_url = os.getenv("APP_URL", "http://localhost:5000")
    password = os.getenv("APP_SHARED_PASSWORD", "changeme")

    async def login(page):
        await page.goto(f"{app_url}/login")
        await page.fill("#password", password)
        await page.click("text=Login")

    await login(page1)
    await login(page2)

    await page1.fill("#video-url", "https://www.bilibili.com/video/BV1xx411c7mD")
    await page1.click("#load-video")

    await page1.click("#play-btn")
    await page2.wait_for_timeout(1000)
    await page1.click("#pause-btn")
    await page2.wait_for_timeout(1000)

    status_text = await page2.text_content("#video-message")
    assert status_text and "Status" in status_text
