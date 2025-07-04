from data.ingredients import Ingredients
import pytest
import allure
from data.response import StatusCode, ResponseText
from generation import generate_user_data_without_field
from methods.create_order import create_order_with_auth, create_order_without_auth


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.story("Успешное создание заказа")
    @allure.title("Создание заказа с авторизацией и корректными ингредиентами")
    def test_create_order_with_auth_success(self, registered_user):
        response = create_order_with_auth(
            registered_user["access_token"],
            Ingredients.correct_ingredients_hash_data["ingredients"]
        )

        with allure.step("Проверка статус кода"):
            assert response.status_code == StatusCode.OK, (
                f"Ожидался статус код {StatusCode.OK}, получен {response.status_code}"
            )

        with allure.step("Проверка тела ответа"):
            response_data = response.json()

            # Проверка успешности операции
            assert "success" in response_data, "Отсутствует поле 'success'"
            assert response_data["success"] is True, "Поле 'success' должно быть True"

            # Проверка названия бургера
            assert "name" in response_data, "Отсутствует поле 'name'"
            assert response_data["name"] == "Space астероидный бургер", (
                f"Неверное название бургера: {response_data['name']}"
            )

            # Проверка данных заказа
            assert "order" in response_data, "Отсутствует объект 'order'"
            assert "number" in response_data["order"], "Отсутствует номер заказа"
            assert isinstance(response_data["order"]["number"], int), "Номер заказа должен быть числом"

    @allure.story("Неуспешное создание заказа")
    @allure.title("Попытка создания заказа без авторизации (должна быть ошибка)")
    def test_create_order_without_auth_fail(self):
        response = create_order_without_auth(
            Ingredients.correct_ingredients_hash_data["ingredients"]
        )

        assert response.status_code == StatusCode.UNAUTHORIZED, (
            f"Ожидался статус код {StatusCode.UNAUTHORIZED}, получен {response.status_code}"
        )
        assert ResponseText.NOT_AUTHORIZED in response.json()["message"], (
            "Сообщение об ошибке должно указывать на необходимость авторизации"
        )

    @allure.story("Неуспешное создание заказа")
    @allure.title("Попытка создания заказа без ингредиентов (с авторизацией)")
    def test_create_order_without_ingredients_fail(self, registered_user):
        response = create_order_with_auth(
            registered_user["access_token"],
            Ingredients.empty_ingredients_data["ingredients"]
        )

        assert response.status_code == StatusCode.BAD_REQUEST
        assert ResponseText.MISSING_INGREDIENTS in response.json()["message"]

    @allure.story("Неуспешное создание заказа")
    @allure.title("Попытка создания заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients_fail(self, registered_user):
        response = create_order_with_auth(
            registered_user["access_token"],
            Ingredients.incorrect_ingredients_hash_data["ingredients"]
        )

        assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR