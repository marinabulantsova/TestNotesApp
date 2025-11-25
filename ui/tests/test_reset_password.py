from playwright.sync_api import expect
from ui.pages.reset_password_page import ResetPasswordPage
from api.config import TEMP_USER_NEW_PASSWORD
import allure

@allure.label("layer", "web")
@allure.feature("Сброс пароля")
@allure.story("Успешный сброс пароля")

def test_reset_password(temp_user_with_inbox, mailslurp_client):
    inbox_api, wait_api, email_api = mailslurp_client
    login_page = temp_user_with_inbox["login_page"]

    with allure.step("Клик на Forgot password"):
        forgot_password_page = login_page.click_forgot_password()

    with allure.step("Проверка открытия страницы Forgot password"):
        expect(forgot_password_page.title).to_be_visible()

    with allure.step("Отправка формы для получения ссылки для сброса пароля"):
        forgot_password_page.send_me_reset_link(email=temp_user_with_inbox["email"])
        expect(forgot_password_page.alert_message).to_contain_text("An e-mail with a link to reset the password has been sent to ")
        emails = wait_api.wait_for_email_count(inbox_id=temp_user_with_inbox["inbox_id"], count=1, timeout=30000)
        email_preview = emails[0]
        email_full = email_api.get_email(email_preview.id)
        reset_token = email_full.body.strip().split("/")[-1]

    with allure.step("Переход по ссылке сброса пароля"):
        reset_page = ResetPasswordPage(login_page.page)
        reset_page.open(reset_token)

    with allure.step("Обновление пароля"):
        reset_page.update_password({"password": TEMP_USER_NEW_PASSWORD, "confirm_password": TEMP_USER_NEW_PASSWORD})

    with allure.step("Проверка возможности войти в новым паролем"):
        login_page = reset_page.goto_login()
        home_page = login_page.login({"email": temp_user_with_inbox["email"], "password": TEMP_USER_NEW_PASSWORD})
        expect(home_page.header.link_profile).to_be_visible()

    with (allure.step("Проверка невозможности войти со старым паролем")):
        home_page.header.logout()
        login_page = home_page.goto_login()
        login_page.login({"email": temp_user_with_inbox["email"], "password": temp_user_with_inbox["password"]})
        expect(login_page.alert_message).to_have_text("Incorrect email address or password")

    temp_user_with_inbox["password"] = TEMP_USER_NEW_PASSWORD






