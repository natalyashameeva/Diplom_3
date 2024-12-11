import pytest
from selenium import webdriver
from page_objects.forgot_password_page import ForgotPasswordPage
import time
import requests
from page_objects.account_page import AccountPage
from page_objects.login_page import LoginPage
from page_objects.main_page import MainPage
from page_objects.order_feed_page import OrderFeedPage
import allure

BASE_URL = "https://stellarburgers.nomoreparties.site"

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Неизвестный браузер: {request.param}")

    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def forgot_password_url():
    return "https://stellarburgers.nomoreparties.site/forgot-password"

@pytest.fixture
@allure.step("Страница восстановления пароля")
def reset_password_url():
    return "reset-password"

@pytest.fixture
def test_email():
    return "test@example.com"

@pytest.fixture
def forgot_password_page(driver):
    forgot_password_page = ForgotPasswordPage(driver)
    driver.get(BASE_URL)
    forgot_password_page.open_recovery_page()
    return forgot_password_page


API_BASE_URL = "https://stellarburgers.nomoreparties.site/api"
TEST_USER_DATA = {
    "email": f"testuser_{int(time.time())}@example.com",
    "password": "testpassword123",
    "name": "Test User"
}

@pytest.fixture(scope="session")
@allure.step(" Создание тестового пользователя через API и возврат его данных")
def create_test_user():
    user_data = TEST_USER_DATA.copy()
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json=user_data)
        if response.status_code == 403:
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
        if 'access_token' in locals() and access_token:
            headers = {"Authorization": f"Bearer {access_token}"}
            delete_response = requests.delete(f"{API_BASE_URL}/auth/user", headers=headers)
            if delete_response.status_code != 202:
                print("Не удалось удалить пользователя.")




@pytest.fixture
@allure.step("Логин пользователя")
def login_user(driver, create_test_user):
    user_data, _ = create_test_user
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    login_page.login(user_data["email"], user_data["password"])
    return driver

@pytest.fixture
def account_page(login_user):
    return AccountPage(login_user)

@pytest.fixture
def main_page(login_user):
    return MainPage(login_user)

@pytest.fixture
def order_feed_page(login_user):
    return OrderFeedPage(login_user)