import pytest
import uuid
from api.endpoints.auth_api import AuthApi
from api.endpoints.notes_api import NotesApi
from api.endpoints.profile_api import ProfileApi
from mailslurp_client import Configuration, ApiClient, InboxControllerApi, WaitForControllerApi, EmailControllerApi
from api.config import BASE_URL, TEMP_USER_PASSWORD, TEMP_USER_NAME, DATA_LOGIN, DATA_CREATE_NOTE
from dotenv import load_dotenv
import os

load_dotenv()
MAILSLURP_API_KEY = os.getenv("MAILSLURP_API_KEY")

@pytest.fixture(scope="session")
def auth_token():
    auth_api = AuthApi(BASE_URL)
    response = auth_api.login(DATA_LOGIN)
    yield response.json()["data"]["token"]
    auth_api.logout()

@pytest.fixture(scope="session")
def notes_api(auth_token):
    return NotesApi(BASE_URL, auth_token)

@pytest.fixture(scope="function")
def note_id(auth_token):
    notes_api = NotesApi(BASE_URL, auth_token)
    response = notes_api.create_note(DATA_CREATE_NOTE)
    id = response.json()["data"]["id"]
    yield id
    notes_api.delete_note(id)

@pytest.fixture(scope="function")
def temp_user():
    auth_api = AuthApi(BASE_URL)
    name = TEMP_USER_NAME
    email = f"temp_user_{uuid.uuid4().hex[:6]}@gmail.com"
    password = TEMP_USER_PASSWORD

    register_response = auth_api.register({"name": name, "email": email, "password": password})
    assert register_response.status_code == 201
    response = auth_api.login({"email": email, "password": password})
    token = response.json()["data"]["token"]
    user_data = { "email": email, "name": name, "password": password, "token": token}
    yield user_data

    try:
        response = auth_api.login({"email": user_data["email"], "password": user_data["password"]})
        if response.status_code == 200:
            new_token = response.json()["data"]["token"]
            profile_api = ProfileApi(BASE_URL, new_token)
            profile_api.delete_profile()
    except Exception as e:
        print(f"Не удалось удалить пользователя: {e}")

@pytest.fixture(scope="session")
def mailslurp_client():
    config = Configuration()
    config.api_key['x-api-key'] = MAILSLURP_API_KEY
    api_client = ApiClient(configuration=config)
    return InboxControllerApi(api_client), WaitForControllerApi(api_client), EmailControllerApi(api_client)

@pytest.fixture(scope="function")
def temp_user_with_inbox(mailslurp_client):
    inbox_api, wait_api, email_api = mailslurp_client
    auth_api = AuthApi(BASE_URL)
    inbox = inbox_api.create_inbox()

    name = TEMP_USER_NAME
    email = inbox.email_address
    password = TEMP_USER_PASSWORD

    auth_api.register({"name": name, "email": email, "password": password})
    response = auth_api.login({"email": email, "password": password})
    token = response.json()["data"]["token"]
    user_data = {"name": name, "email": email, "password": password, "token": token, "inbox_id": inbox.id}
    yield user_data

    try:
        response = auth_api.login({"email": user_data["email"], "password": user_data["password"]})
        if response.status_code == 200:
            new_token = response.json()["data"]["token"]
            profile_api = ProfileApi(BASE_URL, new_token)
            profile_api.delete_profile()
    except Exception as e:
        print(f"Не удалось удалить пользователя: {e}")
    inbox_api.delete_inbox(inbox.id)