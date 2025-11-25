# Демо-проект по тестированию API и UI Приложения с заметками
## Тестирование API
[Swagger Docs](https://practice.expandtesting.com/notes/api/api-docs/#/)  
Схема тестирования API
```mermaid
classDiagram
    direction TB
    BaseApi <|-- AuthApi
    BaseApi <|-- PasswordApi
    BaseApi <|-- ProfileApi
    BaseApi <|-- NotesApi

    %% Базовый класс
    class BaseApi {
        +base_url
        +session
        +get()
        +post()
        +put()
        +patch()
        +delete(path)
    }

    class AuthApi {
        +register()
        +login()
        +logout()
    }

    class PasswordApi {
        +forgot_password()
        +verify_reset_token()
        +reset_password()
        +change_password()
    }

    class ProfileApi {
        +get_profile()
        +update_profile()
        +delete_profile()
    }

    class NotesApi {
        +create_note()
        +get_all_notes()
        +get_note()
        +update_note()
        +update_status_note()
        +delete_note()
    }
```
Каждый метод тестировался только с валидными данными
## Тестирование UI
[Приложение](https://practice.expandtesting.com/notes/app)  

Схема тестирования UI
```mermaid
classDiagram
  direction LR
  namespace PAGES {
    class BasePage {
        +page: Page
        +open_page(path: string)
    }
    class RegisterPage {
        +open()
        +register()
        +goto_login()
    }
    class LoginPage {
        +open()
        +login()
        +goto_register()
        +click_forgot_password()
    }
    class ForgorPasswordPage {
        +open()
        +send_me_reset_link()
        +goto_login()
    }
    class ResetPasswordPage {
        +open()
        +update_password()
        +goto_login()
    }
    class HomePage {
        +open()
        +goto_login()
        +goto_register()
        +click_add_note()
        +get_last_added_note_id()
        +get_note_by_id()
        +search_notes()
        +click_category_notes()
    }
    class NotePage {
        +open()
        +click_edit()
        +click_delete()
        +set_completed()
        +unset_completed()
    }
    class ProfilePage {
        +open()
        +get_tab_account_details()
        +get_tab_change_password()
    }
  }

  namespace COMPONENTS {
    class HeaderComponent {
        +logout()
        +goto_home()
        +goto_profile()
    }
    class NoteAddComponent {
        +fill_note_form()
        +click_create()
        +click_cancel()
    }
    class NoteEditComponent {
        +fill_note_form()
        +click_save()
        +click_cancel()
    }
    class NoteCardComponent {
        +click_view()
        +click_edit()
        +click_delete()
        +set_completed()
        +unset_completed()
    }
    class DeleteDialogComponent {
        +confirm_deletion()
        +cancel_deletion()
    }
    class AccountDetailsComponent {
        +update_profile()
        +get_profile_data()
        +click_delete()
    }
    class ChangePasswordComponent {
        +change_password()
    }
  }


  BasePage <|-- RegisterPage
  BasePage <|-- LoginPage
  BasePage <|-- HomePage
  BasePage <|-- NotePage
  BasePage <|-- ProfilePage
  BasePage <|-- ForgorPasswordPage
  BasePage <|-- ResetPasswordPage


  HomePage *-- "1" HeaderComponent 
  HomePage *-- "many" NoteCardComponent 
  NotePage *-- "1" HeaderComponent 
  ProfilePage *-- "1" HeaderComponent 
  ProfilePage *-- "1" AccountDetailsComponent 
  ProfilePage *-- "1" ChangePasswordComponent

  HomePage ..> NoteAddComponent : click_add_note()
  HomePage ..> NoteCardComponent: get_note_by_id()
  HomePage ..> RegisterPage: goto_register()
  HomePage ..> LoginPage: goto_login()
  NoteCardComponent ..> NoteEditComponent : click_edit()
  NoteCardComponent ..> DeleteDialogComponent : click_delete()
  NoteCardComponent ..> NotePage : click_view()
  
  NotePage ..> NoteEditComponent : click_edit()
  NotePage ..> DeleteDialogComponent : click_delete()

  AccountDetailsComponent ..> DeleteDialogComponent : click_delete()
  LoginPage ..> HomePage : successful login()
  LoginPage ..> RegisterPage : goto_register()
  LoginPage ..> ForgorPasswordPage: click_forgot_password()
  ForgorPasswordPage ..> LoginPage: goto_login()
  ResetPasswordPage ..> LoginPage: goto_login()
  RegisterPage ..> LoginPage : goto_login()
  HeaderComponent ..> HomePage : goto_home()
  HeaderComponent ..> ProfilePage : goto_profile()

```
**Демонстрация применения основных техник тест-дизайна**
### Классы эквивалентности и граничные значения
Пример: форма редактирования профиля

![img.png](.github/assets/img_1.png)
Запуск тестов: `pytest .\ui\tests\test_profile.py::test_update_profile -v`

### Попарное тестирование 
Пример: Заполнение формы добавления заметки

| Поле        | Значения                               | Количество вариантов |
|-------------|----------------------------------------|----------------------|
| Category    | Home, Work, Personal                   | 3                    |
| Completed   | отмечен / не отмечен                   | 2                    |
| Title       | Валидный / Пустой / Короткий / Длинный | 4                    |
| Description | Валидный / Пустой / Короткий / Длинный | 4                    |

Всего комбинаций: 3\*2\*4\*4 = 96

Для попарного тестирования: 16 комбинаций 

```
valid valid Personal False
short short Work False
long long Home False
empty empty Home True
empty long Work True
long short Personal True
short valid Home True
valid empty Work True
empty short Home False
valid long Home True
short empty Personal False
long valid Work True
empty valid Personal True
long empty Home True
short long Personal True
valid short Home True
```
Запуск тестов: `pytest .\ui\tests\test_notes.py::test_add_note -v`

### Таблица принятия решений
Пример: Заполнение формы смена пароля  

рассмотрены не все возможные варианты, а основные пользовательские сценарии: форма не заполнена, потом отдельно обрабатываем каждую ошибку

![img_1.png](.github/assets/img_4.png)
Запуск тестов: ` pytest .\ui\tests\test_profile.py::test_change_password -v`

### Диаграмма состояний и переходов
Пример: Жизненный цикл заметки

```mermaid
stateDiagram-v2
    direction LR
    state "Не существует" as DoesNotExist
    state "Создание" as Creating
    state "Редактирование" as Editing

    state "Существует" as Exists {
        direction LR
        state "Не выполнена" as NotCompleted
        state "Выполнена" as Completed

        NotCompleted --> Completed : Поставить галочку Completed
        Completed --> NotCompleted : Снять галочку Completed
    }

    DoesNotExist --> Creating : Клик на + Add Note

    Creating --> DoesNotExist : Клик на Cancel
    Creating --> NotCompleted : Валидное заполнение<br>completed не проставлен<br>клик на Create
    Creating --> Completed : Валидное заполнение<br>completed проставлен<br>клик на Create

    Exists --> DoesNotExist : Клик на Delete и подтверждение
    Exists --> Editing : Клик на Edit

    Editing --> Exists : Клик на Cancel
    Editing --> NotCompleted : Валидное редактирование<br>completed не проставлен<br>Клик на Save
    Editing --> Completed : Валидное редактирование<br>completed проставлен<br>Клик на Save
```
Таблица состояний и переходов
![img.png](.github/assets/img_5.png)
Запуск тестов: `pytest .\ui\tests\test_life_cycle_note.py -v`

