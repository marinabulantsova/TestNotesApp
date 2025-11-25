from playwright.sync_api import expect
from ui.config import DATA_LOGIN
import allure

@allure.label("layer", "web")
@allure.feature("Вход в систему")
@allure.story("Успешный вход в систему")
def test_login(login_page):
    with allure.step(f"Вход в систему для пользователя: {DATA_LOGIN["email"]}"):
        home_page = login_page.login(DATA_LOGIN)
    with allure.step(f"Проверка открытия домашней страницы"):
        expect(home_page.header.link_profile).to_be_visible()