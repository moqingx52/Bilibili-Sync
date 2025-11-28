import pytest_asyncio
from playwright.async_api import async_playwright


@pytest_asyncio.fixture(scope="session")
async def browser_contexts():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-setuid-sandbox",
            ],
        )
        ctx1 = await browser.new_context()
        ctx2 = await browser.new_context()
        yield ctx1, ctx2
        await ctx1.close()
        await ctx2.close()
        await browser.close()
