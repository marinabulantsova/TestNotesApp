from playwright.sync_api import Page, Locator

class DeleteDialogComponent:
    def __init__(self, page: Page):
        self.page = page
        self.button_confirm = self.page.get_by_test_id("note-delete-confirm")
        self.button_cancel = self.page.get_by_test_id("note-delete-cancel-2")

    def confirm_deletion(self):
        self.button_confirm.click()

    def cancel_deletion(self):
        self.button_cancel.click()