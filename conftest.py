import pytest
from selenium import webdriver
from page_objects.forgot_password_page import ForgotPasswordPage
import time
import requests

@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    # Фикстура для запуска браузера на основе параметров
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Неизвестный браузер: {request.param}")

    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    # Возвращает базовый URL приложения
    return "https://stellarburgers.nomoreparties.site"


@pytest.fixture
def forgot_password_url():
    return "https://stellarburgers.nomoreparties.site/forgot-password"

@pytest.fixture
def reset_password_url():
    # Фикстура для URL страницы восстановления пароля
    return "reset-password"

@pytest.fixture
def test_email():
    # Фикстура для тестового email в восстановлении пароля
    return "test@example.com"

@pytest.fixture
def forgot_password_page(browser, base_url):
    # Фикстура для страницы восстановления пароля
    forgot_password_page = ForgotPasswordPage(browser)
    browser.get(base_url)
    forgot_password_page.open_recovery_page()
    return forgot_password_page


#создание юзера через апи

API_BASE_URL = "https://stellarburgers.nomoreparties.site/api"
TEST_USER_DATA = {
    "email": f"testuser_{int(time.time())}@example.com",  # Генерирует уникальный email
    "password": "testpassword123",
    "name": "Test User"
}

@pytest.fixture(scope="session")
def create_test_user():
    # Создает тестового пользователя через API и возвращает его данные.
    user_data = TEST_USER_DATA.copy()
    try:
        # Попытка регистрации пользователя
        response = requests.post(f"{API_BASE_URL}/auth/register", json=user_data)
        if response.status_code == 403:  # Если пользователь уже существует
            print("Пользователь уже существует, попытка авторизации.")
            login_response = requests.post(
                f"{API_BASE_URL}/auth/login",
                json={
                    "email": user_data["email"],
                    "password": user_data["password"]
                }
            )
            login_response.raise_for_status()
            access_token = login_response.json().get("accessToken")
        else:
            response.raise_for_status()
            access_token = response.json().get("accessToken")

        if not access_token:
            raise ValueError("Не удалось получить токен доступа.")

        yield user_data, access_token

    finally:
        # Удаление пользователя после завершения тестов
        if 'access_token' in locals() and access_token:
            headers = {"Authorization": f"Bearer {access_token}"}
            delete_response = requests.delete(f"{API_BASE_URL}/auth/user", headers=headers)
            if delete_response.status_code != 202:
                print("Не удалось удалить пользователя.")