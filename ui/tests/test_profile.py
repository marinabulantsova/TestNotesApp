from ui.pages.profile_page import ProfilePage
from ui.pages.login_page import LoginPage
from ui.config import DATA_UPDATE_PASSWORD, DATA_LOGIN
from playwright.sync_api import expect
import pytest
import allure

with open("data/data_for_test_update_profile.csv", "r", encoding="utf-8-sig") as f:
    data_for_test_update_profile = [line.strip().split(';') for line in f]

@allure.label("layer", "web")
@allure.feature("Профиль пользователя")
class TestProfilePage:
    @allure.story("Обновление данных о пользователя")
    @pytest.mark.parametrize(
        "name, phone, company, feedback_name, feedback_phone, feedback_company",
        [pytest.param(*data, id = " ".join(data[:3])) for data in data_for_test_update_profile]
    )
    def test_update_profile(self, profile_page, name, phone, company, feedback_name, feedback_phone, feedback_company, request):
        current_id = request.node.callspec.id
        allure.dynamic.title(f"Обновление данных: {current_id}")

        with allure.step("Подготовка данных"):
            account_details_tab = profile_page.get_tab_account_details()
            current_data_profile = account_details_tab.get_profile_data()
            data_update_profile = {"name": name, "phone": phone, "company": company}
            new_data_profile = current_data_profile | data_update_profile

        with allure.step("Обновление данных профиля"):
            account_details_tab.update_profile(data_update_profile)

        if not feedback_name and not feedback_phone and not feedback_company:
            with allure.step("Проверка сообщение об успехе"):
                expect(account_details_tab.alert_message).to_have_text("Profile updated successful")
            with allure.step("Проверка обновлённых данных"):
                expect(account_details_tab.input_id).to_have_value(new_data_profile["id"])
                expect(account_details_tab.input_email).to_have_value(new_data_profile["email"])
                expect(account_details_tab.input_phone).to_have_value(new_data_profile["phone"])
                expect(account_details_tab.input_name).to_have_value(new_data_profile["name"])
                expect(account_details_tab.input_company).to_have_value(new_data_profile["company"])
        else:
            with allure.step("Проверка сообщений об ошибках заполнения полей"):
                expect(account_details_tab.feedback_name).to_have_text(feedback_name)
                expect(account_details_tab.feedback_phone).to_have_text(feedback_phone)
                expect(account_details_tab.feedback_company).to_have_text(feedback_company)

    @allure.story("Изменение пароля")
    @pytest.mark.parametrize(
        "current_password, new_password, confirm_password, feedback_current_password, feedback_new_password, feedback_confirm_password, alert_message",
        [
            pytest.param("", "", "", "Current password is required", "New password is required", "Confirm password is required", "", id="all fields empty"),
            pytest.param("12345", "1234567", "1234567", "Current password should be between 6 and 30 characters", "", "", "", id="invalid current password"),
            pytest.param("12345678", "1234567", "1234567", "", "", "", "The current password is incorrect", id="incorrect current password"),
            pytest.param("123456", "12345", "12345", "", "New password should be between 6 and 30 characters", "", "", id="invalid new password"),

            pytest.param("123456", "123456", "123456", "", "", "", "The new password should be different from the current password", id="new password equal current password"),
            pytest.param("123456", "1234567", "12345678", "", "", "Passwords don't match!", "", id="confirm password don't match new password"),
            pytest.param("123456", "1234567", "1234567", "", "", "", "The password was successfully updated", id="successfully updated"),
        ]
    )
    def test_change_password(self, profile_page, page, current_password, new_password, confirm_password, feedback_current_password, feedback_new_password, feedback_confirm_password, alert_message, request):
        current_id = request.node.callspec.id
        allure.dynamic.title(f"Изменение пароля: {current_id}")

        with allure.step("Подготовка данных"):
            change_password_tab = profile_page.get_tab_change_password()
            data_update_password = {
                "current_password": current_password,
                "new_password": new_password,
                "confirm_password": confirm_password
            }

        with allure.step("Изменение пароля"):
            change_password_tab.change_password(data_update_password)

        if alert_message == "The password was successfully updated":
            with allure.step("Проверка сообщения об успешном изменении пароля"):
                expect(change_password_tab.alert_message).to_have_text(alert_message)

            with allure.step("Проверка невозможности войти в систему со старым паролем"):
                login_page = LoginPage(page)
                login_page.open()
                login_page.login(DATA_LOGIN)
                expect(login_page.alert_message).to_have_text("Incorrect email address or password")

            with allure.step("Проверка возможности войти в систему с новым паролем"):
                home_page = login_page.login({"email": DATA_LOGIN["email"], "password": DATA_UPDATE_PASSWORD["new_password"]})
                expect(home_page.header.link_home).to_be_visible()

            with allure.step("Изменение пароля обратно"):
                home_page.header.goto_profile().get_tab_change_password().change_password({
                    "current_password": DATA_UPDATE_PASSWORD["new_password"],
                    "new_password": DATA_UPDATE_PASSWORD["current_password"],
                    "confirm_password": DATA_UPDATE_PASSWORD["current_password"]
                })
            expect(change_password_tab.alert_message).to_have_text("The password was successfully updated")
        elif alert_message:
            with allure.step("Проверка сообщения о неуспешном изменении пароля"):
                expect(change_password_tab.alert_message).to_have_text(alert_message)
        else:
            with allure.step("Проверка сообщений об ошибках заполнения полей"):
                expect(change_password_tab.feedback_current_password).to_have_text(feedback_current_password)
                expect(change_password_tab.feedback_new_password).to_have_text(feedback_new_password)
                expect(change_password_tab.feedback_confirm_password).to_have_text(feedback_confirm_password)

    @allure.story("Выход из профиля")
    def test_logout(self, fresh_authorized_page):
        profile_page = ProfilePage(fresh_authorized_page)
        profile_page.open()

        with allure.step("Клик на Logout"):
            profile_page.header.logout()

        with allure.step("Проверка перанаправления на домашнюю страницу"):
            expect(fresh_authorized_page.get_by_text("Welcome to Notes App")).to_be_visible()