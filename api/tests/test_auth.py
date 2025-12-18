from api.endpoints.auth_api import AuthApi
from api.endpoints.profile_api import ProfileApi
from api.config import BASE_URL, DATA_LOGIN, DATA_REGISTER
from api.schemas.users import UserRegisterResponse, UserLoginResponse
from api.response import ResponseWrapper
import allure

@allure.label("layer", "rest")
@allure.feature("Аутентификация")
class TestAuth:

    @allure.story("Регистрация")
    def test_register(self):
        auth_api = AuthApi(BASE_URL)

        with allure.step(f"Регистрация пользователя: {DATA_REGISTER["email"]}"):
            response = auth_api.register(DATA_REGISTER)

        ResponseWrapper(response) \
            .assert_status_code(201) \
            .validate(UserRegisterResponse) \
            .assert_json_value("data.name", DATA_REGISTER["name"]) \
            .assert_json_value("data.email", DATA_REGISTER["email"])

        with allure.step(f"Вход в систему для пользователя: {DATA_REGISTER["email"]}"):
            login_response = auth_api.login({"email": DATA_REGISTER["email"], "password": DATA_REGISTER["password"]})

        ResponseWrapper(login_response) \
            .assert_status_code(200) \
            .validate(UserLoginResponse) \
            .assert_json_value("data.name", DATA_REGISTER["name"]) \
            .assert_json_value("data.email", DATA_REGISTER["email"])

        with allure.step("Удаление созданного пользователя"):
            profile_api = ProfileApi(BASE_URL, login_response.json()["data"]["token"])
            delete_response = profile_api.delete_profile()
            ResponseWrapper(delete_response) \
                .assert_status_code(200)

    @allure.story("Вход в систему")
    def test_login(self):
        auth_api = AuthApi(BASE_URL)
        with allure.step(f"Вход в систему для пользователя: {DATA_LOGIN["email"]}"):
            response = auth_api.login(DATA_LOGIN)

        ResponseWrapper(response) \
            .assert_status_code(200) \
            .validate(UserLoginResponse) \
            .assert_json_value("data.email", DATA_LOGIN["email"])

    @allure.story("Выход из системы")
    def test_logout(self, temp_user):
        token = temp_user["token"]
        auth_api = AuthApi(BASE_URL, token)

        with allure.step(f"Выход из системы для пользователя: {temp_user["email"]}"):
            response = auth_api.logout()
            ResponseWrapper(response) \
                .assert_status_code(200)

        with allure.step("Проверка невозможности получить данные по старому токену аутентификации"):
            profile_api = ProfileApi(BASE_URL, token)
            response = profile_api.get_profile()
            ResponseWrapper(response) \
                .assert_status_code(401)