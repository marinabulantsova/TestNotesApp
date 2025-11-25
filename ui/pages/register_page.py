from ui.pages.base_page import BasePage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages.login_page import LoginPage

class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = self.page.get_by_role("heading", name="Register")
        self.input_name = self.page.get_by_test_id("register-name")
        self.input_email = self.page.get_by_test_id("register-email")
        self.input_password = self.page.get_by_test_id("register-password")
        self.input_confirm_password = self.page.get_by_test_id("register-confirm-password")
        self.button_register = self.page.get_by_role("button", name="Register")
        self.alert_success = self.page.locator(".alert.alert-success")

        self.link_login = self.page.get_by_test_id("login-view")

    def open(self):
        self.open_page("/register")

    def _fill_form(self, register_data):
        if "name" in register_data:
            self.input_name.fill(register_data["name"])
        if "email" in register_data:
            self.input_email.fill(register_data["email"])
        if "password" in register_data:
            self.input_password.fill(register_data["password"])
        if "confirm_password" in register_data:
            self.input_confirm_password.fill(register_data["confirm_password"])
        return self

    def _click_register(self):
        self.button_register.click()

    def register(self, register_data):
        return self._fill_form(register_data)._click_register()

    def goto_login(self):
        from ui.pages.login_page import LoginPage

        self.link_login.click()
        return LoginPage(self.page)