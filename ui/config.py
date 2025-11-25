BASE_URL = "https://practice.expandtesting.com/notes/app"

DATA_LOGIN = {
    "email": "marina@mail.ru",
    "password": "123456"
}

DATA_LOGOUT = {
    "email": "logount@mail.ru",
    "password": "1234567"
}

DATA_REGISTER = {
    "name": "temp_user",
    "email": "temp_user@gmail.com",
    "password": "123456",
    "confirm_password": "123456"
}

DATA_UPDATE_PROFILE = {
    "name": "Marina",
    "phone": "+79109109191"
}

DATA_CREATE_NOTE = {
    "title": "Title",
    "description": "Description",
    "category": "Home",
    "completed": False
}

DATA_CREATE_NOT_COMPLETED_NOTE = {
    "title": "Title",
    "description": "Description",
    "category": "Home",
    "completed": False
}

DATA_CREATE_COMPLETED_NOTE = {
    "title": "Title",
    "description": "Description",
    "category": "Home",
    "completed": True
}

DATA_UPDATE_NOTE = {
    "title": "TitleUpdate",
    "description": "DescriptionUpdate",
    "category": "Personal",
    "completed": False
}

DATA_UPDATE_COMPLETED_NOTE = {
    "title": "TitleUpdate",
    "description": "DescriptionUpdate",
    "category": "Personal",
    "completed": True
}

DATA_UPDATE_NOT_COMPLETED_NOTE = {
    "title": "TitleUpdate",
    "description": "DescriptionUpdate",
    "category": "Personal",
    "completed": False
}

DATA_UPDATE_STATUS_NOTE = {
    "completed": True
}

DATA_UPDATE_PASSWORD = {
    "current_password": "123456",
    "new_password": "1234567",
    "confirm_password": "1234567"
}

CATEGORY_COLORS = {
    "Home": "rgb(255, 145, 0)",
    "Work": "rgb(92, 107, 192)",
    "Personal": "rgb(50, 140, 160)",
}

COMPLETED_COLOR = "rgba(40, 46, 41, 0.6)"

SEARCH_TEXT = "title"

LIST_NOTES_FOR_SEARCH = [
    {
        "title": "test title",
        "description": "test description",
        "category": "Home",
        "completed": False
    },
    {
        "title": "test title1",
        "description": "test description1",
        "category": "Home",
        "completed": False
    },
    {
        "title": "test Title",
        "description": "test Description",
        "category": "Work",
        "completed": False
    },
    {
        "title": "test",
        "description": "test",
        "category": "Personal",
        "completed": False
    }
]

LIST_NOTES_FOR_FILTER = [
    {
        "title": "Home title 1",
        "description": "Home description 1",
        "category": "Home",
        "completed": False
    },
    {
        "title": "Home title 2",
        "description": "Home description 2",
        "category": "Home",
        "completed": False
    },
    {
        "title": "Work title 1",
        "description": "Work description 1",
        "category": "Work",
        "completed": False
    },
    {
        "title": "Work title 2",
        "description": "Work description 2",
        "category": "Work",
        "completed": False
    },
    {
        "title": "Personal title 1",
        "description": "Personal description 1",
        "category": "Personal",
        "completed": False
    },
    {
        "title": "Personal title 2",
        "description": "Personal description 2",
        "category": "Personal",
        "completed": False
    }
]