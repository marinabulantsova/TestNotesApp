from ui.components.delete_dialog_component import DeleteDialogComponent
from ui.components.header_component import HeaderComponent
from ui.components.note_edit_component import NoteEditComponent

class NotePage:
    def __init__(self, page):
        self.page = page
        self.header = HeaderComponent(self.page)
        self.title = self.page.get_by_test_id("note-card-title")
        self.description = self.page.get_by_test_id("note-card-description")
        self.updated_at= self.page.get_by_test_id("note-card-updated-at")
        self.completed = self.page.get_by_test_id("toggle-note-switch")

        self.button_view = self.page.get_by_test_id("note-view")
        self.button_edit = self.page.get_by_test_id("note-edit")
        self.button_delete = self.page.get_by_test_id("note-delete")

    def open(self, note_id):
        self.page.open(f"/{note_id}")

    def click_edit(self):
        self.button_edit.click()
        return NoteEditComponent(self.page)

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