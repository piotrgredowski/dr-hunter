# from playwright.async_api import async_playwright
from typing import Type, cast
from playwright.sync_api import sync_playwright
from playwright.sync_api._context_manager import PlaywrightContextManager
import os
import asyncio
from playwright.sync_api import Page


class Options:
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")
    browser = os.getenv("BROWSER", "chromium")


class Paths:
    main_page = "https://mol.medicover.pl/Users/Account/AccessDenied?ReturnUrl=%2F"
    popup_open_path = '//*[@id="oidc-submit"]'
    username_path = '//*[@id="UserName"]'
    password_path = '//*[@id="Password"]'
    login_button_path = '//*[@id="loginBtn"]'

    change_language_path = '//*[@id="header_language_bar"]/a[1]'

    schedule_visit_link = "https://mol.medicover.pl/pfm-menu-en/"

    specialist_button_selector = "#orthopedist-otherproblem > a"

    specialist_url = "https://mol.medicover.pl/MyVisits?bookingTypeId=2&specializationId=44058&selectedSpecialties=44058&pfm=1"

    book_path = "/html/body/div[3]/div/div[4]/div/div/div/div[2]/div/article/div[18]/div[1]/div/a"

    search_selector = "#advancedSearchForm > form > div:nth-child(2) > div > button"


class Medicover:
    def __init__(self, options: Type[Options], paths: Type[Paths]):
        self._options = options
        self._paths = paths

    def login(self, page: Page):
        with page.expect_popup() as popup_info:
            page.click(Paths.popup_open_path)
        popup = popup_info.value
        popup.wait_for_load_state("networkidle")
        username = popup.locator(Paths.username_path)
        username.type(Options.login or "")
        popup.wait_for_timeout(100)
        password = popup.locator(Paths.password_path)
        password.type(Options.password or "")

        login_button = popup.locator(Paths.login_button_path)
        login_button.focus()
        popup.wait_for_load_state("networkidle")

        login_button.click()
        try:
            popup.wait_for_load_state("networkidle")
            # popup.wait_for_timeout(2000)
            popup.close()
        except:
            pass

    def change_language(self, page: Page):
        page.wait_for_load_state("networkidle")
        # page.locator(Paths.change_language_selector).click()
        page.locator(Paths.change_language_path).click()
        page.wait_for_load_state("networkidle")
        pass

    def go_to_schedule_visit(self, page: Page):
        page.wait_for_timeout(1000)
        page.goto(Paths.schedule_visit_link)

    def print_days(self, days):
        for day in days:
            title = day.query_selector(".visitListDate").inner_text()
            dates = day.query_selector_all(".slot-time")

            print(f"==================== {title} ====================")
            for date in dates:
                print(f"- {date.inner_text()}")

    def go_to_visits(self, page: Page):
        # self.go_to_schedule_visit(page)
        page.wait_for_load_state("networkidle")
        # page.goto(Paths.schedule_visit_link)
        # page.wait_for_load_state("networkidle")
        # page.query_selector(Paths.specialist_button_selector).click()
        # page.wait_for_load_state("networkidle")
        page.goto(Paths.specialist_url)
        page.wait_for_load_state("networkidle")
        page.query_selector(Paths.search_selector).click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)
        days = page.query_selector_all("app-visit-list>div:has(.visitListDate)")
        self.print_days(days)

    def main(self):
        with sync_playwright() as p:

            browser_func = getattr(p, Options.browser)

            browser = browser_func.launch(headless=Options.headless)

            context = browser.new_context()
            page = context.new_page()
            page.goto(Paths.main_page)

            self.login(page)
            self.change_language(page)

            page.wait_for_load_state("networkidle")

            self.go_to_visits(page)

            title = page.title()

            browser.close()


if __name__ == "__main__":
    Medicover(options=Options, paths=Paths).main()
