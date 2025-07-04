import requests
import allure
from data.endpoints import DataForUser
from data.url import URL

# методы для тестирования создания заказа
@allure.step("Создание заказа с авторизацией")
def create_order_with_auth(auth_token, ingredients):
    """Создание заказа с авторизацией"""
    return requests.post(
        URL.main_url + DataForUser.CREATE_ORDER,
        headers={"Authorization": auth_token},
        json={"ingredients": ingredients}
    )

@allure.step("Создание заказа без авторизации")
def create_order_without_auth(ingredients):
    """Создание заказа без авторизации"""
    return requests.post(
        URL.main_url + DataForUser.CREATE_ORDER,
        json={"ingredients": ingredients}
    )

