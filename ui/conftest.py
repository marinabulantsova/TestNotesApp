import pytest
from playwright.sync_api import Playwright, Browser, BrowserContext, Page, expect, TimeoutError
from ui.pages.home_page import HomePage
from ui.pages.login_page import LoginPage
from ui.pages.profile_page import ProfilePage
from ui.pages.register_page import RegisterPage
from ui.config import DATA_LOGIN, DATA_LOGOUT

from mailslurp_client import Configuration, ApiClient, InboxControllerApi, WaitForControllerApi, EmailControllerApi
from api.config import TEMP_USER_PASSWORD, TEMP_USER_NAME, TEMP_USER_NEW_PASSWORD
from dotenv import load_dotenv
import re
import os


load_dotenv()
MAILSLURP_API_KEY = os.getenv("MAILSLURP_API_KEY")

def _block_ads(context: BrowserContext):
    context.route(re.compile(r"(ads|doubleclick|banner|pop|metrics)", re.I), lambda route: route.abort())

@pytest.fixture(scope="session")
def storage_state_path(playwright: Playwright, tmp_path_factory):
    state_path = tmp_path_factory.mktemp("auth") / "auth.json"

    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(DATA_LOGIN)
    page.wait_for_url("**/notes/app")

    context.storage_state(path=str(state_path))
    context.close()
    browser.close()

    return str(state_path)

@pytest.fixture(scope="function")
def authorized_context(browser: Browser, storage_state_path: str):
    context = browser.new_context(storage_state=storage_state_path)
    _block_ads(context)

    yield context

    context.close()

@pytest.fixture(scope="function")
def authorized_page(authorized_context: BrowserContext):
    page = authorized_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def home_page(authorized_page: Page):
    home_page = HomePage(authorized_page)
    home_page.open()
    final_state_locator = home_page.locator_note_cards.first.or_(home_page.empty_list_notes)
    expect(final_state_locator).to_be_visible()
    return home_page

@pytest.fixture(scope="function")
def profile_page(authorized_page: Page):
    profile_page = ProfilePage(authorized_page)
    profile_page.open()
    expect(profile_page.title).to_be_visible()
    return profile_page

@pytest.fixture(scope="function")
def page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    _block_ads(context)

    yield page

    context.close()

@pytest.fixture(scope="function")
def login_page(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    expect(login_page.title).to_be_visible()
    return login_page

@pytest.fixture(scope="function")
def register_page(page: Page):
    register_page = RegisterPage(page)
    register_page.open()
    expect(register_page.title).to_be_visible()
    return register_page

@pytest.fixture(scope="function")
def fresh_authorized_page(browser: Browser):
    context = browser.new_context()
    _block_ads(context)
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(DATA_LOGOUT)
    page.wait_for_url("**/notes/app")

    _block_ads(context)

    yield page

    context.close()

@pytest.fixture(scope="function")
def note_factory(home_page: HomePage):
    created_notes_ids = []

    def _create_note(note_data):
        final_state_locator = home_page.locator_note_cards.first.or_(home_page.empty_list_notes)
        expect(final_state_locator).to_be_visible()
        initial_cnt = home_page.locator_note_cards.count()

        home_page.click_add_note().fill_note_form(note_data).click_create()

        expect(home_page.locator_note_cards).to_have_count(initial_cnt + 1)
        note_id = home_page.get_last_added_note_id(note_data.get("completed", False))
        created_notes_ids.append(note_id)
        return note_id

    yield _create_note

    if created_notes_ids:
        home_page.header.goto_home()
        home_page.click_categoty_notes("all")
        final_state_locator = home_page.locator_note_cards.first.or_(home_page.empty_list_notes)
        expect(final_state_locator).to_be_visible()
        for note_id in created_notes_ids:
            try:
                home_page.get_note_by_id(note_id).click_delete().confirm_deletion()
            except TimeoutError:
                print(" Заметка, вероятно, уже удалена тестом")

@pytest.fixture(scope="session")
def mailslurp_client():
    config = Configuration()
    config.api_key['x-api-key'] = MAILSLURP_API_KEY
    api_client = ApiClient(configuration=config)
    return InboxControllerApi(api_client), WaitForControllerApi(api_client), EmailControllerApi(api_client)

@pytest.fixture(scope="function")
def temp_user_with_inbox(mailslurp_client, register_page):
    inbox_api, wait_api, email_api = mailslurp_client
    inbox = inbox_api.create_inbox()

    name = TEMP_USER_NAME
    email = inbox.email_address
    password = TEMP_USER_PASSWORD

    register_page.register({"name": name, "email": email, "password": password, "confirm_password": password})
    expect(register_page.alert_success).to_contain_text("User account created successfully")

    login_page = register_page.goto_login()

    user_data = {
        "login_page": login_page,
        "email": email,
        "password": password,
        "name": name,
        "inbox_id": inbox.id
    }
    yield user_data

    login_page.open()
    home_page = login_page.login({"email": email, "password": user_data["password"]})
    profile_page = home_page.header.goto_profile()
    profile_page.tab_account_details.click_delete().confirm_deletion()
    inbox_api.delete_inbox(inbox.id)