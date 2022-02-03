from playwright.async_api import async_playwright
import os
import asyncio


class Options:
    headless = os.getenv("HEADLESS", "true").lower() == "true"


class Links:
    main_page = "https://mol.medicover.pl/Users/Account/AccessDenied?ReturnUrl=%2F"
    popup_open_path = '//*[@id="oidc-submit"]'


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=Options.headless)
        page = await browser.new_page()
        await page.goto(Links.main_page)
        await page.click(Links.popup_open_path)
        title = await page.title()
        print(title)
        await browser.close()


asyncio.run(main())
