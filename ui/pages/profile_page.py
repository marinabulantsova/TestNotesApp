from ui.pages.base_page import BasePage
from ui.components.account_details_component import AccountDetailsComponent
from ui.components.change_password_component import ChangePasswordComponent
from ui.components.header_component import HeaderComponent


class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.title = self.page.get_by_role("heading", name="Profile settings")
        self.tab_account_details = AccountDetailsComponent(page)
        self.tab_change_password = ChangePasswordComponent(page)
        self.button_account_details = self.page.get_by_role("button", name="Account details")
        self.button_change_password = self.page.get_by_role("button", name="Change password")

    def open(self):
        self.open_page("/profile")

    def get_tab_account_details(self):
        self.button_account_details.click()
        return self.tab_account_details

    def get_tab_change_password(self):
        self.button_change_password.click()
        return self.tab_change_password


