from api.endpoints.profile_api import ProfileApi
from api.config import BASE_URL, DATA_UPDATE_PROFILE
import allure

@allure.label("layer", "rest")
@allure.feature("Профиль пользователя")

class TestProfile:
    @allure.story("Получение данных по пользователю")
    def test_get_profile(self, temp_user):
        profile_api = ProfileApi(BASE_URL, temp_user["token"])

        with allure.step(f"Запрос на получение данных по пользователю: {temp_user["email"]}"):
            response = profile_api.get_profile()

        with allure.step("Проверка ответа (код 200 и данные)"):
            assert response.status_code == 200
            assert response.json()["data"]["name"] == temp_user["name"]
            assert response.json()["data"]["email"] == temp_user["email"]

    @allure.story("Обновление данных пользователя")
    def test_update_profile(self, temp_user):
        profile_api = ProfileApi(BASE_URL, temp_user["token"])
        new_data = DATA_UPDATE_PROFILE

        with allure.step(f"Запрос на обновление данных пользователя: {temp_user["email"]}"):
            response = profile_api.update_profile(new_data)

        with allure.step("Проверка ответа (код 200 и обновлённые данные)"):
            assert response.status_code == 200
            assert response.json()["data"]["name"] == new_data["name"]
            assert response.json()["data"]["phone"] == new_data["phone"]

    @allure.story("Удаление аккаунта")
    def test_delete_profile(self, temp_user):
        profile_api = ProfileApi(BASE_URL, temp_user["token"])
        with allure.step(f"Запрос на удаление профиля пользователя: {temp_user["email"]}"):
            response = profile_api.delete_profile()

        with allure.step("Проверка ответа (код 200)"):
            assert response.status_code == 200