from playwright.sync_api import Page


class NoteAddComponent:
    def __init__(self, page: Page):
        self.page = page
        self.title = self.page.locator(".modal-title.h5.ps-2")
        self.select_category = self.page.get_by_test_id("note-category")
        self.checkbox_completed = self.page.get_by_test_id("note-completed")
        self.input_title = self.page.get_by_test_id("note-title")
        self.feedback_title = self.input_title.locator("xpath=..").locator(".invalid-feedback")
        self.input_description = self.page.get_by_test_id("note-description")
        self.feedback_description = self.input_description.locator("xpath=..").locator(".invalid-feedback")
        self.button_cancel = self.page.get_by_role("button", name="Cancel")
        self.button_create = self.page.get_by_role("button", name="Create")

    def fill_note_form(self, note_data):
        if "category" in note_data:
            self.select_category.select_option(note_data["category"])
        if "completed" in note_data:
            if note_data["completed"]:
                self.checkbox_completed.check()
            else:
                self.checkbox_completed.uncheck()
        if "title" in note_data:
            self.input_title.fill(note_data["title"])
        if "description" in note_data:
            self.input_description.fill(note_data["description"])
        return self

    def click_create(self):
        self.button_create.click()

    def click_cancel(self):
        self.button_cancel.click()
