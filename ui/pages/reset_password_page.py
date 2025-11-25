from ui.pages.base_page import BasePage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages.login_page import LoginPage

class ResetPasswordPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = self.page.get_by_role("heading", name="Reset Password")
        self.input_password = self.page.get_by_test_id("password")
        self.input_confirm_password = self.page.get_by_test_id("confirm-password")
        self.button_update = self.page.get_by_role("button", name = "Update")
        self.link_login = self.page.get_by_test_id("login")

    def open(self, token):
        self.open_page(f'/reset-password/{token}')

    def _fill_form(self, update_data):
        if "password" in update_data:
            self.input_password.fill(update_data["password"])
        if "confirm_password" in update_data:
            self.input_confirm_password.fill(update_data["confirm_password"])
        return self

    def _click_update(self):
        self.button_update.click()

    def update_password(self, update_data):
        self._fill_form(update_data)._click_update()

    def goto_login(self):
        from ui.pages.login_page import LoginPage

        self.link_login.click()
        return LoginPage(self.page)