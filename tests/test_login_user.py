import pytest
import allure
from data.response import StatusCode
from methods.create_user import (
    login_user,
    login_with_wrong_email,
    login_with_wrong_password,
    login_without_email,
    login_without_password,
    login_with_empty_fields,
)


@allure.feature("Логин пользователя")
class TestLoginUser:
    @allure.story("Успешный логин")
    @allure.title("Проверка успешного входа с валидными данными")
    def test_login_success(self, create_new_user):
        user_data = create_new_user["user_data"]

        with allure.step("Выполнение запроса на логин"):
            response = login_user(user_data["email"], user_data["password"])

        with allure.step("Проверка статус кода"):
            assert response.status_code == StatusCode.OK

        with allure.step("Проверка тела ответа"):
            response_data = response.json()

            # Проверка общей структуры ответа
            assert "success" in response_data
            assert response_data["success"] is True

            # Проверка accessToken
            assert "accessToken" in response_data
            assert isinstance(response_data["accessToken"], str)
            assert len(response_data["accessToken"]) > 0
            assert response_data["accessToken"].startswith("Bearer ")
            assert len(response_data["accessToken"].split(".")) == 3  # JWT состоит из 3 частей

            # Проверка refreshToken
            assert "refreshToken" in response_data
            assert isinstance(response_data["refreshToken"], str)
            assert len(response_data["refreshToken"]) > 0

            # Проверка данных пользователя
            assert "user" in response_data
            user_info = response_data["user"]
            assert isinstance(user_info, dict)

            assert "email" in user_info
            assert isinstance(user_info["email"], str)
            assert user_info["email"] == user_data["email"]

            assert "name" in user_info
            assert isinstance(user_info["name"], str)
            assert user_info["name"] == user_data["name"]


    @allure.story("Неуспешный логин")
    @allure.title("Попытка входа с неверным email")
    def test_login_wrong_email_fail(self, create_new_user):
        user_data = create_new_user["user_data"]
        response = login_with_wrong_email(user_data["email"], user_data["password"])

        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json()["success"] is False
        assert "email or password are incorrect" in response.json()["message"].lower()

    @allure.story("Неуспешный логин")
    @allure.title("Попытка входа с неверным паролем")
    def test_login_wrong_password_fail(self, create_new_user):
        user_data = create_new_user["user_data"]
        response = login_with_wrong_password(user_data["email"], user_data["password"])

        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json()["success"] is False
        assert "email or password are incorrect" in response.json()["message"].lower()

    @allure.story("Неуспешный логин")
    @allure.title("Попытка входа без email")
    def test_login_missing_email_fail(self, create_new_user):
        user_data = create_new_user["user_data"]
        response = login_without_email(user_data["password"])

        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json()["success"] is False
        assert "email or password are incorrect" in response.json()["message"].lower()

    @allure.story("Неуспешный логин")
    @allure.title("Попытка входа без пароля")
    def test_login_missing_password_fail(self, create_new_user):
        user_data = create_new_user["user_data"]
        response = login_without_password(user_data["email"])

        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json()["success"] is False
        assert "email or password are incorrect" in response.json()["message"].lower()

    @allure.story("Неуспешный логин")
    @allure.title("Попытка входа с пустыми полями")
    def test_login_empty_fields_fail(self):
        response = login_with_empty_fields()

        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json()["success"] is False
        assert "email or password are incorrect" in response.json()["message"].lower()
