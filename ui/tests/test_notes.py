from playwright.sync_api import expect
import pytest
from ui.config import CATEGORY_COLORS, COMPLETED_COLOR, SEARCH_TEXT, LIST_NOTES_FOR_SEARCH, LIST_NOTES_FOR_FILTER
from allpairspy import AllPairs
import allure

parameters_add_notes = [
    ["valid", "short", "long", "empty"],  # Title
    ["valid", "short", "long", "empty"],  # Description
    ["Personal", "Work", "Home"],  # Category
    [False, True],  # Completed
]
pairwise_combinations = list(AllPairs(parameters_add_notes))

DATA_TITLE = {
    "valid": ("Title", ""),
    "short": ("ti", "Title should be between 4 and 100 characters"),
    "long": ("t" * 110, "Title should be between 4 and 100 characters"),
    "empty": ("", "Title is required"),
}

DATA_DESCRIPTION = {
    "valid": ("Description", ""),
    "short": ("de", "Description should be between 4 and 1000 characters"),
    "long": ("d" * 1010, "Description should be between 4 and 1000 characters"),
    "empty": ("", "Description is required")
}

@allure.label("layer", "web")
@allure.feature("Работа со страницей заметок")
class TestHomePage:
    @allure.story("Создание заметки")
    @pytest.mark.parametrize(
        "title, description, category, completed",
        [pytest.param(*pair, id=", ".join(map(str, pair))) for pair in pairwise_combinations]
    )
    def test_add_note(self, home_page, title, description, category, completed):
        allure.dynamic.title(f"Создание заметки: {category}, {completed}, {title}, {description}")

        with allure.step("Подготовка данных"):
            title, feedback_title = DATA_TITLE[title]
            description, feedback_description = DATA_DESCRIPTION[description]
            note_data = {
                "category": category,
                "completed": completed,
                "title": title,
                "description": description,
            }
        with allure.step("Считываем текущее количество заметок"):
            final_state_locator = home_page.locator_note_cards.first.or_(home_page.empty_list_notes)
            expect(final_state_locator).to_be_visible()
            initial_cnt = home_page.locator_note_cards.count()

        with allure.step("Открытие и заполнение формы, клик на Create"):
            note_form = home_page.click_add_note()
            note_form.fill_note_form(note_data).click_create()

        if not feedback_description and not feedback_title:
            with allure.step("Проверка, что количество заметок увеличилось на 1"):
                expect(home_page.locator_note_cards).to_have_count(initial_cnt + 1)

            note_id = home_page.get_last_added_note_id(note_data.get("completed", False))
            new_note = home_page.get_note_by_id(note_id)
            result_data = new_note.get_note_data()

            with allure.step("Проверка данных созданной заметки"):
                assert result_data["title"] == note_data["title"]
                assert result_data["description"] == note_data["description"]
                expected_color = COMPLETED_COLOR if note_data.get("completed", False) else CATEGORY_COLORS[note_data["category"]]
                assert result_data["color"] == expected_color

            with allure.step("Удаление заметки"):
                new_note.click_delete().confirm_deletion()
        else:
            with allure.step("Проверка сообщений об ошибках заполнения полей"):
                expect(note_form.feedback_title).to_have_text(feedback_title)
                expect(note_form.feedback_description).to_have_text(feedback_description)

    @allure.story("Поиск заметок")
    def test_search_notes(self, note_factory, home_page):
        with allure.step("Подготовка данных"):
            search_text = SEARCH_TEXT
            for note_data in LIST_NOTES_FOR_SEARCH:
                note_factory(note_data)

        with allure.step("Расчёт статистики по отобранным данным"):
            all_notes_cnt, filter_notes_cnt = home_page.get_search_notes_cnt(search_text)

        with allure.step("Клик на Search"):
            home_page.search_notes(search_text)

        with allure.step("Проверка сообщения"):
            expect(home_page.page.get_by_text("Search Results for ")).to_be_visible()

        with allure.step("Проверка совпадения количества отобранных заметок"):
            searched_notes_cnt, filter_searched_notes_cnt = home_page.get_search_notes_cnt(search_text)
            assert filter_searched_notes_cnt == searched_notes_cnt == filter_notes_cnt

    @allure.story("Фильтрация заметок по категориям")
    @pytest.mark.parametrize(
        "category",
        [
            pytest.param("Work", id="Work"),
            pytest.param("Personal", id="Personal"),
            pytest.param("Home", id="Home"),
        ]
    )
    def test_filter_category(self, note_factory, home_page, category):
        allure.dynamic.title(f"Фильтрация заметок по категории: {category}")
        with allure.step("Подготовка данных"):
            for note_data in LIST_NOTES_FOR_FILTER:
                note_factory(note_data)

        with allure.step("Расчёт статистики по данной категории"):
            all_notes_cnt, filter_notes_cnt = home_page.get_filter_notes_cnt(category)

        with allure.step(f"Клик на категорию {category}"):
            home_page.click_categoty_notes(category)

        with allure.step("Проверка совпадения количества отобранных заметок"):
            searched_notes_cnt, filter_searched_notes_cnt = home_page.get_filter_notes_cnt(category)
            assert filter_searched_notes_cnt == searched_notes_cnt == filter_notes_cnt