import allure
from api.endpoints.password_api import PasswordApi
from api.endpoints.auth_api import AuthApi
from api.config import BASE_URL, TEMP_USER_NEW_PASSWORD

@allure.label("layer", "rest")
@allure.feature("Изменение пароля")
class TestPassword:

    @allure.story("Сброс пароля через почту")
    def test_reset_password(self, mailslurp_client, temp_user_with_inbox):
        inbox_api, wait_api, email_api = mailslurp_client
        password_api = PasswordApi(BASE_URL)

        with allure.step(f"Забыли пароль :{temp_user_with_inbox["email"]}"):
            response = password_api.forgot_password({"email": temp_user_with_inbox["email"]})
            assert response.status_code == 200

        with allure.step("Считываем из последнего письма токен для сброса пароля"):
            emails = wait_api.wait_for_email_count(inbox_id=temp_user_with_inbox["inbox_id"], count=1, timeout=30000)
            email_preview = emails[0]
            email_full = email_api.get_email(email_preview.id)
            reset_token = email_full.body.strip().split("/")[-1]

        with allure.step("Проверка корректности токена для сброса пароля"):
            response = password_api.verify_reset_token({"token": reset_token})
            assert response.status_code == 200

        with allure.step("Изменение пароля по токену"):
            new_password = TEMP_USER_NEW_PASSWORD
            response = password_api.reset_password({"token": reset_token, "newPassword": new_password})
            assert response.status_code == 200

        auth_api = AuthApi(BASE_URL)

        with allure.step("Проверка успешного входа с новым паролем"):
            response = auth_api.login({"email": temp_user_with_inbox["email"], "password": new_password})
            assert response.status_code == 200

        with allure.step("Проверка невозможности входа со старым паролем"):
            response = auth_api.login({"email": temp_user_with_inbox["email"], "password": temp_user_with_inbox["password"]})
            assert response.status_code == 401

        temp_user_with_inbox["password"] = new_password

    @allure.story("Изменение пароля по текущему паролю")
    def test_change_password(self, temp_user):
        password_api = PasswordApi(BASE_URL, temp_user["token"])

        with allure.step(f"Изменение пароля для пользователя: {temp_user["email"]}"):
            new_password = TEMP_USER_NEW_PASSWORD
            response = password_api.change_password({"currentPassword": temp_user["password"], "newPassword": new_password})
            assert response.status_code == 200

        auth_api = AuthApi(BASE_URL)
        with allure.step("Проверка успешного входа с новым паролем"):
            response = auth_api.login({"email": temp_user["email"], "password": new_password})
            assert response.status_code == 200

        with allure.step("Проверка невозможности входа со старым паролем"):
            response = auth_api.login({"email": temp_user["email"], "password": temp_user["password"]})
            assert response.status_code == 401

        temp_user["password"] = new_password