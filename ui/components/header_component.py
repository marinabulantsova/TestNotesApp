from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.pages.home_page import HomePage
    from ui.pages.profile_page import ProfilePage

class HeaderComponent:
    def __init__(self, page):
        self.page = page
        self.link_profile = self.page.get_by_test_id("profile")
        self.button_logout = self.page.get_by_role("button", name="Logout")
        self.link_home = self.page.get_by_test_id("home")

    def logout(self):
        self.button_logout.click()

    def goto_home(self):
        from ui.pages.home_page import HomePage

        self.link_home.click()
        return HomePage(self.page)

    def goto_profile(self):
        from ui.pages.profile_page import ProfilePage

        self.link_profile.click()
        return ProfilePage(self.page)