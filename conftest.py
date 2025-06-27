import pytest
import allure
from generation import generate_user_data
from methods.create_user import create_user

@pytest.fixture
def create_new_user():
    """Фикстура для создания нового пользователя"""
    with allure.step("Создание нового пользователя"):
        user_data = generate_user_data()
        response = create_user(user_data)
        return {
            "user_data": user_data,
            "response": response
        }


@pytest.fixture
def registered_user(create_new_user):
    """Фикстура, которая возвращает зарегистрированного пользователя с токеном."""
    response = create_new_user["response"]

    if response.status_code != 200:
        pytest.fail(f"Ошибка регистрации! Код: {response.status_code}, Ответ: {response.text}")

    return {
        "access_token": response.json()["accessToken"]
    }

