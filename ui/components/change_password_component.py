from playwright.sync_api import Page


class ChangePasswordComponent:
    def __init__(self, page: Page):
        self.page = page
        self.input_current_password = self.page.get_by_test_id("current-password")
        self.feedback_current_password = self.input_current_password.locator('xpath=..').locator('.invalid-feedback')
        self.input_new_password = self.page.get_by_test_id("new-password")
        self.feedback_new_password = self.input_new_password.locator("xpath=..").locator(".invalid-feedback")
        self.input_confirm_password = self.page.get_by_test_id("confirm-password")
        self.feedback_confirm_password = self.input_confirm_password.locator("xpath=..").locator(".invalid-feedback")
        self.button_change_password = self.page.get_by_role("button", name="Change password")
        self.button_update_password = self.page.get_by_role("button", name="Update password")
        self.alert_message = self.page.get_by_test_id("alert-message")

    def _fill_form(self, password_data):
        if "current_password" in password_data:
            self.input_current_password.fill(password_data["current_password"])
        if "new_password" in password_data:
            self.input_new_password.fill(password_data["new_password"])
        if "confirm_password" in password_data:
            self.input_confirm_password.fill(password_data["confirm_password"])
        return self

    def _click_update_password(self):
        self.button_update_password.click()

    def change_password(self, password_data):
        self._fill_form(password_data)._click_update_password()

