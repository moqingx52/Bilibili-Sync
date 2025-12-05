import os

import pytest

pytestmark = [
    pytest.mark.skipif(not os.getenv("RUN_E2E"), reason="Set RUN_E2E=1 to run browser chat history test"),
    pytest.mark.asyncio,
]


async def test_chat_history_on_refresh(browser_contexts):
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

    await page1.fill("#chat-input", "history msg")
    await page1.click("#chat-send")
    await page2.wait_for_selector("#chat-messages .chat-message:has-text('history msg')", timeout=2000)

    # Refresh page2 to simulate late join/refresh
    await page2.reload()
    await login(page2)
    await page2.wait_for_selector("#chat-messages .chat-message:has-text('history msg')", timeout=2000)
