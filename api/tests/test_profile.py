from api.endpoints.auth_api import AuthApi
from api.endpoints.profile_api import ProfileApi
from api.config import BASE_URL, DATA_UPDATE_PROFILE
from api.schemas.users import UserDataResponse
from api.response import ResponseWrapper
import allure

@allure.label("layer", "rest")
@allure.feature("Профиль пользователя")

class TestProfile:
    @allure.story("Получение данных по пользователю")
    def test_get_profile(self, temp_user):
        profile_api = ProfileApi(BASE_URL, temp_user["token"])

        with allure.step(f"Запрос на получение данных по пользователю: {temp_user["email"]}"):
            response = profile_api.get_profile()

        ResponseWrapper(response) \
            .assert_status_code(200) \
            .validate(UserDataResponse) \
            .assert_json_value("data.name", temp_user["name"]) \
            .assert_json_value("data.email", temp_user["email"])

    @allure.story("Обновление данных пользователя")
    def test_update_profile(self, temp_user):
        profile_api = ProfileApi(BASE_URL, temp_user["token"])
        new_data = DATA_UPDATE_PROFILE

        with allure.step(f"Запрос на обновление данных пользователя: {temp_user["email"]}"):
            response = profile_api.update_profile(new_data)

        ResponseWrapper(response) \
            .assert_status_code(200) \
            .validate(UserDataResponse) \
            .assert_json_value("data.name", new_data["name"]) \
            .assert_json_value("data.phone", new_data["phone"])

    @allure.story("Удаление аккаунта")
    def test_delete_profile(self, temp_user):
        profile_api = ProfileApi(BASE_URL, temp_user["token"])
        with allure.step(f"Запрос на удаление профиля пользователя: {temp_user["email"]}"):
            response = profile_api.delete_profile()

        ResponseWrapper(response) \
            .assert_status_code(200)

        with allure.step("Проверка, что нет возможности войти после удаления"):
            auth_api = AuthApi(BASE_URL)
            response = auth_api.login({"email": temp_user["email"], "password": temp_user["password"]})
            ResponseWrapper(response) \
                .assert_status_code(401)