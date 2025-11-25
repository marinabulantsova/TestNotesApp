from ui.components.delete_dialog_component import DeleteDialogComponent
from ui.components.note_edit_component import NoteEditComponent
from ui.pages.note_page import NotePage


class NoteCardComponent:
    def __init__(self, root_locator, page):
        self.page = page
        self.root_locator = root_locator
        self.title = self.root_locator.get_by_test_id("note-card-title")
        self.description = self.root_locator.get_by_test_id("note-card-description")
        self.updated_at= self.root_locator.get_by_test_id("note-card-updated-at")
        self.completed = self.root_locator.get_by_test_id("toggle-note-switch")

        self.button_view = self.root_locator.get_by_test_id("note-view")
        self.button_edit = self.root_locator.get_by_test_id("note-edit")
        self.button_delete = self.root_locator.get_by_test_id("note-delete")

    def click_edit(self):
        self.button_edit.click()
        return NoteEditComponent(self.page)

    def click_view(self):
        self.button_view.click()
        return NotePage(self.page)

    def click_delete(self):
        self.button_delete.click()
        return DeleteDialogComponent(self.page)

    def set_completed(self):
        self.completed.check()

    def unset_completed(self):
        self.completed.uncheck()

    def get_note_data(self):
        return {
            "category": None,
            "title": self.title.text_content(),
            "description": self.description.text_content(),
            "updated_at": self.updated_at.text_content(),
            "completed": self.completed.is_checked(),
            "color": self.title.evaluate(
                "element => window.getComputedStyle(element).getPropertyValue('background-color')"
            )
        }