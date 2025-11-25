from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage
from ui.components.header_component import HeaderComponent
from ui.components.note_card_component import NoteCardComponent
from ui.components.note_add_component import NoteAddComponent
from ui.config import CATEGORY_COLORS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages.login_page import LoginPage
    from ui.pages.register_page import RegisterPage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(self.page)
        self.button_add_note = self.page.get_by_role("button", name="+ Add Note")
        self.locator_note_cards = self.page.get_by_test_id("note-card")
        self.input_search = self.page.get_by_test_id("search-input")
        self.button_search = self.page.get_by_role("button", name="Search")
        self.empty_list_notes = self.page.get_by_test_id("no-notes-message")
        self.link_login = self.page.get_by_role("link", name="Login")
        self.link_register = self.page.get_by_role("link", name="Create an account")

    def open(self):
        self.open_page("")

    def goto_login(self):
        from ui.pages.login_page import LoginPage

        self.link_login.click()
        return LoginPage(self.page)

    def goto_register(self):
        from ui.pages.register_page import RegisterPage

        self.link_register.click()
        return RegisterPage(self.page)

    def click_add_note(self):
        self.button_add_note.click()
        return NoteAddComponent(self.page)

    def get_card_locator_by_id(self, note_id):
        link_locator = self.page.locator(f"a[href='/notes/app/notes/{note_id}']")
        card_locator = self.locator_note_cards.filter(has=link_locator)
        return card_locator

    def get_note_by_id(self, note_id: str):
        return NoteCardComponent(self.get_card_locator_by_id(note_id), self.page)

    def get_last_added_note_id(self, completed):
        if completed:
            filter_condition = self.page.locator('[data-testid="toggle-note-switch"]:checked')
        else:
            filter_condition = self.page.locator('[data-testid="toggle-note-switch"]:not(:checked)')
        return self.locator_note_cards.filter(has=filter_condition).first.get_by_test_id("note-view").get_attribute("href").split("/")[-1]

    def search_notes(self, text):
        self.input_search.fill(text)
        self.button_search.click()

    def get_category_locator(self, category):
        return self.page.get_by_test_id(f"category-{category.lower()}")

    def click_categoty_notes(self, category):
        self.get_category_locator(category).click()

    def get_search_notes_cnt(self, search_text):
        final_state_locator = self.locator_note_cards.first.or_(self.empty_list_notes)
        expect(final_state_locator).to_be_visible()
        all_notes_cnt = self.locator_note_cards.count()
        filter_notes_cnt = sum(
            1 for i in range(all_notes_cnt)
            if search_text.lower() in self.locator_note_cards.nth(i).get_by_test_id("note-card-title").text_content().lower()
            or search_text.lower() in self.locator_note_cards.nth(i).get_by_test_id(
                "note-card-description").text_content().lower()
        )
        return all_notes_cnt, filter_notes_cnt

    def get_filter_notes_cnt(self, category):
        final_state_locator = self.locator_note_cards.first.or_(self.empty_list_notes)
        expect(final_state_locator).to_be_visible()
        all_notes_cnt = self.locator_note_cards.count()
        filter_notes_cnt = sum(
            1 for i in range(all_notes_cnt)
            if self.locator_note_cards.nth(i).get_by_test_id("note-card-title").evaluate(
                "element => window.getComputedStyle(element).getPropertyValue('background-color')"
            ) == CATEGORY_COLORS[category]
        )
        return all_notes_cnt, filter_notes_cnt