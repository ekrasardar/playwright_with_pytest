import time
from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page, request):
        self.page = page
        self.request = request
        self.search_box = page.locator('[name=q]')
        self.search_button = page.get_by_role("button", name="Google Search")

    def google_search_by_name(self, name):
        self.search_box.fill(name)
        self.search_button.click()
