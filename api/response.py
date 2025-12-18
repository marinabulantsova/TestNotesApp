import allure
from typing import Type, TypeVar
from requests import Response
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

class ResponseWrapper:
    def __init__(self, response: Response):
        self.response = response
        self.status_code = response.status_code
        self.text = response.text
        try:
            self.response_json = response.json()
        except ValueError:
            self.response_json = {}

    @allure.step("Проверка статус кода: {expected_code}")
    def assert_status_code(self, expected_code):
        assert self.status_code == expected_code, \
            f"Ожидался статус {expected_code}, но получен {self.status_code}" \
            f"Тело ответа: {self.text[:100]}"
        return self

    def validate(self, schema: Type[T]):
        with allure.step(f"Валидация по схеме: {schema.__name__}"):
            try:
                schema.model_validate(self.response_json)
            except ValidationError as e:
                allure.attach(str(self.response_json), name="Invalid JSON", attachment_type=allure.attachment_type.JSON)
                raise AssertionError(f"Ошибка валидации схемы {schema.__name__}: {e}")
        return self

    @allure.step("Проверка значения поля {key} = {expected_value}")
    def assert_json_value(self, key: str, expected_value):
        value = self.response_json
        for k in key.split('.'):
            value = value.get(k) if isinstance(value, dict) else None

        assert value == expected_value, \
            f"По ключу {key} ожидали {expected_value}, но получили {value}"
        return self

    @allure.step("Проверка наличия объекта с ID: {id} в списке :{key}")
    def assert_id_in_list(self, key, id):
        items = self.response_json.get(key, [])

        exists = any(item.get("id") == id for item in items if isinstance(item, dict))

        assert exists, f"ID {id} не найден в списке {key}"
        return self