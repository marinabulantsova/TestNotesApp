from playwright.sync_api import Page
from ui.components.delete_dialog_component import DeleteDialogComponent


class AccountDetailsComponent:
    def __init__(self, page: Page):
        self.page = page
        self.input_id = self.page.get_by_test_id("user-id")
        self.input_email = self.page.get_by_test_id("user-email")
        self.input_name = self.page.get_by_test_id("user-name")
        self.feedback_name = self.input_name.locator("xpath=..").locator(".invalid-feedback")
        self.input_phone = self.page.get_by_test_id("user-phone")
        self.feedback_phone = self.input_phone.locator("xpath=..").locator(".invalid-feedback")
        self.input_company = self.page.get_by_test_id("user-company")
        self.feedback_company = self.input_company.locator("xpath=..").locator(".invalid-feedback")
        self.button_update = self.page.get_by_role("button", name="Update profile")
        self.alert_message = self.page.get_by_test_id("alert-message")

        self.button_delete = self.page.get_by_test_id("delete-account")
        self.button_confirm = self.page.get_by_test_id("note-delete-confirm")
        self.button_cancel = self.page.get_by_test_id("note-delete-cancel-2")

    def _fill_form(self, profile_data):
        if "name" in profile_data:
            self.input_name.fill(profile_data["name"])
        if "phone" in profile_data:
            self.input_phone.fill(profile_data["phone"])
        if "company" in profile_data:
            self.input_company.fill(profile_data["company"])
        return self

    def _click_update(self):
        self.button_update.click()

    def update_profile(self, profile_data):
        self._fill_form(profile_data)._click_update()

    def get_profile_data(self):
        return {
            "id": self.input_id.input_value(),
            "email": self.input_email.input_value(),
            "name": self.input_name.input_value(),
            "phone": self.input_phone.input_value(),
            "company": self.input_company.input_value()
        }

    def click_delete(self):
        self.button_delete.click()
        return DeleteDialogComponent(self.page)