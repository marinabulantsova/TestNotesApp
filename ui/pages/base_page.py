from playwright.sync_api import Page
from ui.config import BASE_URL

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.alert_message = self.page.get_by_test_id("alert-message")

    def open_page(self, endpoint):
        self.page.goto(BASE_URL + endpoint)
