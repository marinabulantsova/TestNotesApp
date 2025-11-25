from playwright.sync_api import expect
from ui.config import DATA_REGISTER
import allure

@allure.label("layer", "web")
@allure.feature("Регистрация")
@allure.story("Успешная регистрация")
def test_register(register_page):
    with allure.step(f"Регистрация в системе пользователя: {DATA_REGISTER["email"]}"):
        register_page.register(DATA_REGISTER)

    with allure.step("Проверка сообщения об успешной регистрации"):
        expect(register_page.alert_success).to_contain_text("User account created successfully")

    with allure.step("Проверка входа в систему"):
        login_page = register_page.goto_login()
        home_page = login_page.login({"email": DATA_REGISTER["email"], "password": DATA_REGISTER["password"]})
        expect(home_page.header.link_profile).to_be_visible()

    with allure.step("Удаление пользователя"):
        profile_page = home_page.header.goto_profile()
        profile_page.tab_account_details.click_delete().confirm_deletion()

    with allure.step("Проверка невозможности войти в систему после удаления"):
        login_page.open()
        login_page.login({"email": DATA_REGISTER["email"], "password": DATA_REGISTER["password"]})
        expect(login_page.alert_message).to_have_text("Incorrect email address or password")