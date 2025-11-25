from ui.pages.base_page import BasePage
from ui.pages.home_page import HomePage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages.register_page import RegisterPage
    from ui.pages.forgot_password_page import ForgotPasswordPage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.get_by_role("heading", name="Login")
        self.input_email = self.page.locator("#email")
        self.input_password = self.page.locator("#password")
        self.button_login = self.page.get_by_role("button", name="Login")

        self.link_register = self.page.get_by_test_id("register-view")
        self.link_forgot_password = self.page.locator("#forgotPasswordLink")

    def open(self):
        self.open_page("/login")

    def _fill_form(self, login_data):
        if "email" in login_data:
            self.input_email.fill(login_data["email"])
        if "password" in login_data:
            self.input_password.fill(login_data["password"])
        return self

    def _click_login(self):
        self.button_login.click()
        return HomePage(self.page)

    def login(self, login_data):
        return self._fill_form(login_data)._click_login()

    def goto_register(self):
        from ui.pages.register_page import RegisterPage

        self.link_register.click()
        return RegisterPage(self.page)

    def click_forgot_password(self):
        from ui.pages.forgot_password_page import ForgotPasswordPage

        self.link_forgot_password.click()
        return ForgotPasswordPage(self.page)