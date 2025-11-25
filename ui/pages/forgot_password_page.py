from ui.pages.base_page import BasePage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages.login_page import LoginPage

class ForgotPasswordPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = self.page.get_by_role("heading", name="Reset your password")
        self.input_email = self.page.get_by_test_id("forgot-password-email")
        self.button_send_reset_link = self.page.get_by_test_id("forgot-password-submit")
        self.link_login = self.page.get_by_test_id("login-view")

    def open(self):
        self.open_page("/forgot-password")

    def send_me_reset_link(self, email):
        self.input_email.fill(email)
        self.button_send_reset_link.click()

    def goto_login(self):
        from ui.pages.login_page import LoginPage

        self.link_login.click()
        return LoginPage(self.page)