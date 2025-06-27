import pytest
import allure
from data.response import StatusCode
from generation import generate_user_data_without_field
from methods.create_user import create_user, login_user, delete_user


@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.story("Успешное создание пользователя")
    @allure.title("Проверка успешного создания уникального пользователя")
    def test_create_unique_user_success(self, create_new_user):
        response = create_new_user["response"]
        user_data = create_new_user["user_data"]

        with allure.step("Проверка статус кода"):
            assert response.status_code == StatusCode.OK, (
                f"Ожидался статус код {StatusCode.OK}, получен {response.status_code}"
            )

        with allure.step("Проверка тела ответа"):
            response_data = response.json()

            # Проверка успешности операции
            assert "success" in response_data, "В ответе отсутствует ключ 'success'"
            assert response_data["success"] is True, "Поле 'success' должно быть True"

            # Проверка данных пользователя
            assert "user" in response_data, "В ответе отсутствует ключ 'user'"
            assert response_data["user"]["email"] == user_data["email"], "Email не совпадает"
            assert response_data["user"]["name"] == user_data["name"], "Name не совпадает"

            # Проверка токенов
            assert "accessToken" in response_data, "В ответе отсутствует accessToken"
            assert "refreshToken" in response_data, "В ответе отсутствует refreshToken"
            assert response_data["accessToken"].startswith("Bearer "), "accessToken должен начинаться с 'Bearer '"

        # Очистка - удаляем созданного пользователя
        login_response = login_user(user_data["email"], user_data["password"])
        access_token = login_response.json().get("accessToken")
        if access_token:
            delete_user(access_token)

    @allure.story("Создание существующего пользователя")
    @allure.title("Попытка создания уже зарегистрированного пользователя")
    def test_create_existing_user_fail(self, create_new_user):
        user_data = create_new_user["user_data"]
        response = create_user(user_data)  # Пытаемся создать того же пользователя снова

        with allure.step("Проверка статус кода"):
            assert response.status_code == StatusCode.FORBIDDEN, (
                f"Ожидался статус код {StatusCode.FORBIDDEN}, получен {response.status_code}"
            )

        with allure.step("Проверка тела ответа"):
            response_data = response.json()

            # Проверка успешности операции
            assert "success" in response_data, "В ответе отсутствует ключ 'success'"
            assert response_data["success"] is False, "Поле 'success' должно быть False"

            # Проверка сообщения об ошибке
            assert "message" in response_data, "В ответе отсутствует сообщение об ошибке"
            assert response_data["message"] == "User already exists", "Неверное сообщение об ошибке"

        # Очистка
        login_response = login_user(user_data["email"], user_data["password"])
        access_token = login_response.json().get("accessToken")
        if access_token:
            delete_user(access_token)

    @allure.story("Создание пользователя с неполными данными")
    @allure.title("Попытка создания пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fail(self, missing_field):
        user_data = generate_user_data_without_field(missing_field)
        response = create_user(user_data)

        with allure.step(f"Проверка с отсутствующим полем {missing_field}"):
            assert response.status_code == StatusCode.FORBIDDEN, (
                f"Ожидался статус код {StatusCode.FORBIDDEN}, получен {response.status_code}"
            )

            response_data = response.json()

            with allure.step("Проверка тела ответа"):
                assert "success" in response_data, "Отсутствует поле 'success'"
                assert response_data["success"] is False, "Поле 'success' должно быть False"

                assert "message" in response_data, "Отсутствует сообщение об ошибке"
                assert response_data["message"] == "Email, password and name are required fields", (
                    f"Неверное сообщение об ошибке: {response_data['message']}"
                )