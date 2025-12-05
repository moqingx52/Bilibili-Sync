import os

import pytest

pytestmark = [
    pytest.mark.skipif(not os.getenv("RUN_E2E"), reason="Set RUN_E2E=1 to run browser chat unread test"),
    pytest.mark.asyncio,
]


async def test_chat_unread_indicator(browser_contexts):
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

    # Send enough messages to allow scrolling
    for i in range(8):
        await page1.fill("#chat-input", f"msg {i}")
        await page1.click("#chat-send")
    await page2.wait_for_selector("#chat-messages .chat-message", timeout=2000)

    # Scroll up then send another message to trigger indicator
    await page2.eval_on_selector("#chat-messages", "el => { el.scrollTop = 0; }")
    await page1.fill("#chat-input", "new after scroll")
    await page1.click("#chat-send")

    await page2.wait_for_timeout(500)
    indicator_visible = await page2.eval_on_selector("#chat-new-indicator", "el => !el.hidden")
    assert indicator_visible is True
