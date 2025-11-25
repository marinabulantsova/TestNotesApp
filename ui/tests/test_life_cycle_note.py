from playwright.sync_api import expect
import pytest
from ui.config import DATA_CREATE_COMPLETED_NOTE, DATA_CREATE_NOT_COMPLETED_NOTE, CATEGORY_COLORS, COMPLETED_COLOR, \
    DATA_UPDATE_COMPLETED_NOTE, DATA_UPDATE_NOT_COMPLETED_NOTE
import allure

@allure.label("layer", "web")
@allure.feature("Работа с заметкой")

class TestLifeCycleNote:
    @allure.story("Открытие формы для создания заметки")
    def test_open_add_note_form(self, home_page):
        with allure.step("Клик на кнопку +Add Note"):
            note_add_form = home_page.click_add_note()

        with allure.step("Проверка открытия формы"):
            expect(note_add_form.title).to_have_text("Add new note")

    @allure.story("Отмена создания заметки")
    def test_add_note_cancel(self, home_page):
        with allure.step("Считываем текущее количество заметок"):
            final_state_locator = home_page.locator_note_cards.first.or_(home_page.empty_list_notes)
            expect(final_state_locator).to_be_visible()
            initial_cnt = home_page.locator_note_cards.count()

        with allure.step("Открытие формы редактирования"):
            note_add_form = home_page.click_add_note()

        with allure.step("Нажатие на кнопку Cancel"):
            note_add_form.click_cancel()

        with allure.step("Проверка, что количество заметок не изменилось"):
            expect(note_add_form.title).not_to_be_visible()
            expect(home_page.locator_note_cards).to_have_count(initial_cnt)

    @allure.story("Создание заметки")
    @pytest.mark.parametrize(
        "note_data",
        [
            pytest.param(DATA_CREATE_COMPLETED_NOTE, id="completed note"),
            pytest.param(DATA_CREATE_NOT_COMPLETED_NOTE, id="not completed note"),
        ],
    )
    def test_add_note(self, home_page, note_data, request):
        current_id = request.node.callspec.id
        allure.dynamic.title(f"Создание заметки: {current_id}")

        with allure.step("Считываем текущее количество заметок"):
            final_state_locator = home_page.locator_note_cards.first.or_(home_page.empty_list_notes)
            expect(final_state_locator).to_be_visible()
            initial_cnt = home_page.locator_note_cards.count()

        with allure.step("Открытие и заполнение формы, клик на Create"):
            home_page.click_add_note().fill_note_form(note_data).click_create()

        with allure.step("Проверка, что количество заметок увеличилось на 1"):
            expect(home_page.locator_note_cards).to_have_count(initial_cnt + 1)

        with allure.step("Проверка данных созданной заметки"):
            note_id = home_page.get_last_added_note_id(note_data.get("completed", False))
            new_note = home_page.get_note_by_id(note_id)
            result_data = new_note.get_note_data()
            assert result_data["title"] == note_data["title"]
            assert result_data["description"] == note_data["description"]
            expected_color = COMPLETED_COLOR if note_data.get("completed", False) else CATEGORY_COLORS[note_data["category"]]
            assert result_data["color"] == expected_color

        with allure.step("Удаление заметки"):
            new_note.click_delete().confirm_deletion()

    @allure.story("Перевод заметки из статуса not completed в completed")
    def test_not_completed_to_completed(self, home_page, note_factory):
        with allure.step("Создание not completed заметки"):
            note_id = note_factory(DATA_CREATE_NOT_COMPLETED_NOTE)
            note = home_page.get_note_by_id(note_id)

        with allure.step("Перевод заметки из статуса not completed в completed"):
            note.set_completed()

        with allure.step("Проверка изменения статуса на completed"):
            expect(note.title).to_have_css("background-color", COMPLETED_COLOR)
            expect(note.completed).to_be_checked()

    @allure.story("Перевод заметки из статуса completed в not completed")
    def test_completed_to_not_completed(self, home_page, note_factory):
        with allure.step("Создание completed заметки"):
            note_id = note_factory(DATA_CREATE_COMPLETED_NOTE)
            note = home_page.get_note_by_id(note_id)

        with allure.step("Перевод заметки из статуса completed в not completed"):
            note.unset_completed()

        with allure.step("Проверка изменения статуса на not completed"):
            expect(note.completed).not_to_be_checked()

    @allure.story("Открытие формы редактирования заметки")
    @pytest.mark.parametrize(
        "note_data",
        [
            pytest.param(DATA_CREATE_COMPLETED_NOTE, id="completed note"),
            pytest.param(DATA_CREATE_NOT_COMPLETED_NOTE, id="not completed note"),
        ],
    )
    def test_open_edit_form(self, home_page, note_data, note_factory, request):
        current_id = request.node.callspec.id
        allure.dynamic.title(f"Открытие формы редактирования заметки: {current_id}")

        with allure.step("Создание заметки"):
            note_id = note_factory(note_data)
            note = home_page.get_note_by_id(note_id)

        with allure.step("Клик на Edit"):
            edit_form = note.click_edit()

        with allure.step("Проверка открытия формы на редактирование"):
            expect(edit_form.title).to_have_text("Edit note")

        edit_form.click_cancel()

    @allure.story("Отмена редактирования заметки")
    @pytest.mark.parametrize(
        "note_data, data_update_note",
        [
            pytest.param(DATA_CREATE_COMPLETED_NOTE, DATA_UPDATE_NOT_COMPLETED_NOTE, id="completed note"),
            pytest.param(DATA_CREATE_NOT_COMPLETED_NOTE, DATA_UPDATE_COMPLETED_NOTE, id="not completed note"),
        ],
    )
    def test_edit_not_cancel(self, home_page, note_data, data_update_note, note_factory, request):
        current_id = request.node.callspec.id
        allure.dynamic.title(f"Открытие формы редактирования заметки: {current_id}")

        with allure.step("Создание заметки"):
            note_id = note_factory(note_data)
            note = home_page.get_note_by_id(note_id)
            old_data_note = note.get_note_data()

        with allure.step("Открытие и заполнение формы редактирования заметки, клик на Cancel"):
            note.click_edit().fill_note_form(data_update_note).click_cancel()

        with allure.step("Проверка, что данные заметки не изменились"):
            expect(note.title).to_have_text(old_data_note["title"])
            expect(note.description).to_have_text(old_data_note["description"])
            expect(note.title).to_have_css("background-color", old_data_note["color"])

    @allure.story("Редактирование заметки")
    @pytest.mark.parametrize(
        "note_data, data_update_note",
        [
            pytest.param(DATA_CREATE_COMPLETED_NOTE, DATA_UPDATE_COMPLETED_NOTE, id="update completed-completed"),
            pytest.param(DATA_CREATE_NOT_COMPLETED_NOTE, DATA_UPDATE_COMPLETED_NOTE, id="update not_completed-completed"),
            pytest.param(DATA_CREATE_COMPLETED_NOTE, DATA_UPDATE_NOT_COMPLETED_NOTE, id="update completed-not_completed"),
            pytest.param(DATA_CREATE_NOT_COMPLETED_NOTE, DATA_UPDATE_NOT_COMPLETED_NOTE, id="update not_completed-not_completed")
        ],
    )
    def test_edit_note(self, home_page, note_data, data_update_note, note_factory, request):
        current_id = request.node.callspec.id
        allure.dynamic.title(f"Редактирования заметки: {current_id}")

        with allure.step("Создание заметки"):
            note = home_page.get_note_by_id(note_factory(note_data))
            current_data_note = note.get_note_data()

        with allure.step("Открытие и заполнение формы, клик на Save"):
            note.click_edit().fill_note_form(data_update_note).click_save()

        with allure.step("Проверка обновлённых данных"):
            new_data_note = current_data_note | data_update_note
            new_data_note["color"] = COMPLETED_COLOR if new_data_note["completed"] \
                else CATEGORY_COLORS[data_update_note["category"]] if "category" in data_update_note \
                else new_data_note["color"]
            expect(note.title).to_have_text(new_data_note["title"])
            expect(note.description).to_have_text(new_data_note["description"])
            expect(note.title).to_have_css("background-color", new_data_note["color"])
            if new_data_note["completed"]:
                expect(note.completed).to_be_checked()
            else:
                expect(note.completed).not_to_be_checked()

    @allure.story("Удаление заметки")
    @pytest.mark.parametrize(
        "note_data",
        [
            pytest.param(DATA_CREATE_COMPLETED_NOTE, id="completed note"),
            pytest.param(DATA_CREATE_NOT_COMPLETED_NOTE, id="not completed note"),
        ],
    )
    def test_delete_note(self, home_page, note_data, note_factory, request):
        current_id = request.node.callspec.id
        allure.dynamic.title(f"Удаление заметки: {current_id}")

        with allure.step("Создание заметки"):
            note_id = note_factory(note_data)
            note = home_page.get_note_by_id(note_id)

        with allure.step("Считываем текущее количество заметок"):
            final_state_locator = home_page.locator_note_cards.first.or_(home_page.empty_list_notes)
            expect(final_state_locator).to_be_visible()
            initial_cnt = home_page.locator_note_cards.count()

        with allure.step("Клик на Delete c подтверждением"):
            note.click_delete().confirm_deletion()

        with allure.step("Проверка, что количество заметок уменьшилось на 1"):
            expect(home_page.locator_note_cards).to_have_count(initial_cnt - 1)

        with allure.step("Проверка, что заметки нет в списке"):
            expect(home_page.get_card_locator_by_id(note_id)).not_to_be_attached()