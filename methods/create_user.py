import requests
import allure
from data.endpoints import DataForUser
from data.url import URL

# методы для тестирования создания пользователя
@allure.step("Создание пользователя")
def create_user(user_data):
    """Создание пользователя"""
    return requests.post(
        URL.main_url + DataForUser.CREATE_USER,
        json=user_data
    )

def login_user(email, password):
    """Логин пользователя"""
    return requests.post(
        URL.main_url + DataForUser.LOGIN_USER,
        json={"email": email, "password": password}
    )


@allure.step("Удаление пользователя")
def delete_user(auth_token):
    """Удаление пользователя"""
    return requests.delete(
        URL.main_url + DataForUser.DELETE_USER,
        headers={"Authorization": auth_token}
    )


@allure.step("Попытка создания дубликата пользователя")
def create_duplicate_user(user_data):
    """Попытка создать дубликат пользователя"""
    # Сначала создаем пользователя
    create_response = create_user(user_data)
    # Пытаемся создать его снова
    duplicate_response = create_user(user_data)
    return {
        "create_response": create_response,
        "duplicate_response": duplicate_response
    }

# методы для тестирования логина
@allure.step("Попытка логина с неверным email")
def login_with_wrong_email(correct_email, correct_password):
    """Попытка входа с неверным email"""
    wrong_email = "wrong_" + correct_email
    return login_user(wrong_email, correct_password)

@allure.step("Попытка логина с неверным паролем")
def login_with_wrong_password(correct_email, correct_password):
    """Попытка входа с неверным паролем"""
    wrong_password = "wrong_" + correct_password
    return login_user(correct_email, wrong_password)

@allure.step("Попытка логина без email")
def login_without_email(password):
    """Попытка входа без email"""
    return login_user(None, password)

@allure.step("Попытка логина без пароля")
def login_without_password(email):
    """Попытка входа без пароля"""
    return login_user(email, None)

@allure.step("Попытка логина с пустыми полями")
def login_with_empty_fields():
    """Попытка входа с пустыми полями"""
    return login_user("", "")
