from api.config import DATA_CREATE_NOTE, DATA_UPDATE_NOTE, DATA_UPDATE_STATUS_NOTE
from api.response import ResponseWrapper
from api.schemas.notes import NoteResponse, NoteListResponse
import allure

@allure.label("layer", "rest")
@allure.feature("Работа с заметками")
class TestNotes:

    @allure.story("Создание заметки")
    def test_create_note(self, notes_api):
        data = DATA_CREATE_NOTE

        with allure.step(f"Запрос на создание заметки: {data["title"]}"):
            response = notes_api.create_note(data)

        ResponseWrapper(response) \
            .assert_status_code(200) \
            .validate(NoteResponse) \
            .assert_json_value("data.title", data["title"]) \
            .assert_json_value("data.description", data["description"]) \
            .assert_json_value("data.category", data["category"])

    @allure.story("Получение всех заметок")
    def test_get_all_notes(self, notes_api, note_id):
        with allure.step(f"Запрос на получение информации о всех заметках"):
            response = notes_api.get_all_notes()

        ResponseWrapper(response) \
            .assert_status_code(200) \
            .validate(NoteListResponse) \
            .assert_id_in_list("data", note_id)

    @allure.story("Получение заметки по id")
    def test_get_note(self, notes_api, note_id):
        with allure.step(f"Запрос на получение информации о заметке с id: {note_id}"):
            response = notes_api.get_note(note_id)

        ResponseWrapper(response) \
            .assert_status_code(200) \
            .validate(NoteResponse) \
            .assert_json_value("data.id", note_id)

    @allure.story("Обновление заметки по id")
    def test_update_note(self, notes_api, note_id):
        data = DATA_UPDATE_NOTE

        with allure.step(f"Запрос на обновление информации заметки с id: {note_id}"):
            response = notes_api.update_note(note_id, data)

        ResponseWrapper(response) \
            .assert_status_code(200) \
            .validate(NoteResponse) \
            .assert_json_value("data.id", note_id) \
            .assert_json_value("data.title", data["title"]) \
            .assert_json_value("data.description", data["description"]) \
            .assert_json_value("data.category", data["category"]) \
            .assert_json_value("data.completed", False)

    @allure.story("Обновление статуса заметки по id")
    def test_update_status_note(self, notes_api, note_id):
        data = DATA_UPDATE_STATUS_NOTE

        with allure.step(f"Запрос на обновление статуса заметки с id: {note_id}"):
            response = notes_api.update_status_note(note_id, data)

        expected_completed = data["completed"].lower() == "true" if isinstance(data["completed"], str) else data["completed"]
        ResponseWrapper(response) \
            .assert_status_code(200) \
            .validate(NoteResponse) \
            .assert_json_value("data.id", note_id) \
            .assert_json_value("data.completed", expected_completed)

    @allure.story("Удаление заметки по id")
    def test_delete(self, notes_api, note_id):
        with allure.step(f"Запрос на удаление заметки с id: {note_id}"):
            response = notes_api.delete_note(note_id)

        ResponseWrapper(response) \
            .assert_status_code(200)

        response = notes_api.get_note(note_id)
        ResponseWrapper(response) \
            .assert_status_code(404)