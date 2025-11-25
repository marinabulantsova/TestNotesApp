from api.endpoints.notes_api import NotesApi
from api.config import BASE_URL, DATA_CREATE_NOTE, DATA_UPDATE_NOTE, DATA_UPDATE_STATUS_NOTE
import allure

@allure.label("layer", "rest")
@allure.feature("Работа с заметками")
class TestNotes:

    @allure.story("Создание заметки")
    def test_create_note(self, auth_token):
        notes_api = NotesApi(BASE_URL, auth_token)
        data = DATA_CREATE_NOTE

        with allure.step(f"Запрос на создание заметки: {data["title"]}"):
            response = notes_api.create_note(data)

        with allure.step("Проверка ответа (код 200 и данные)"):
            assert response.status_code == 200
            assert response.json()["data"]["title"] == data['title']
            assert response.json()["data"]["description"] == data['description']
            assert response.json()["data"]["category"] == data['category']

    @allure.story("Получение всех заметок")
    def test_get_all_notes(self, auth_token, note_id):
        notes_api = NotesApi(BASE_URL, auth_token)

        with allure.step(f"Запрос на получение информации о всех заметках"):
            response = notes_api.get_all_notes()

        with allure.step("Проверка ответа (код 200 и данные)"):
            assert response.status_code == 200
            any(map(lambda note: note["id"]==note_id, response.json()["data"]))

    @allure.story("Получение заметки по id")
    def test_get_note(self, auth_token, note_id):
        notes_api = NotesApi(BASE_URL, auth_token)

        with allure.step(f"Запрос на получение информации о заметке с id: {note_id}"):
            response = notes_api.get_note(note_id)

        with allure.step("Проверка ответа (код 200 и данные)"):
            assert response.status_code == 200
            assert response.json()["data"]["id"] == note_id

    @allure.story("Обновление заметки по id")
    def test_update_note(self, auth_token, note_id):
        notes_api = NotesApi(BASE_URL, auth_token)
        data = DATA_UPDATE_NOTE

        with allure.step(f"Запрос на обновление информации заметки с id: {note_id}"):
            response = notes_api.update_note(note_id, data)

        with allure.step("Проверка ответа (код 200 и данные)"):
            assert response.status_code == 200
            assert response.json()["data"]["id"] == note_id
            assert response.json()["data"]["title"] == data['title']
            assert response.json()["data"]["description"] == data['description']
            assert response.json()["data"]["category"] == data['category']
            assert response.json()["data"]["completed"] == False

    @allure.story("Обновление статуса заметки по id")
    def test_update_status_note(self, auth_token, note_id):
        notes_api = NotesApi(BASE_URL, auth_token)
        data = DATA_UPDATE_STATUS_NOTE

        with allure.step(f"Запрос на обновление статуса заметки с id: {note_id}"):
            response = notes_api.update_status_note(note_id, data)

        with allure.step("Проверка ответа (код 200 и данные)"):
            assert response.status_code == 200
            assert response.json()["data"]["id"] == note_id
            assert response.json()["data"]["completed"] == True

    @allure.story("Удаление заметки по id")
    def test_delete(self, auth_token, note_id):
        notes_api = NotesApi(BASE_URL, auth_token)

        with allure.step(f"Запрос на удаление заметки с id: {note_id}"):
            response = notes_api.delete_note(note_id)

        with allure.step("Проверка ответа (код 200 и данные)"):
            assert response.status_code == 200
            response = notes_api.get_note(note_id)
            assert response.status_code == 404