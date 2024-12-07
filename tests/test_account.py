import pytest
from page_objects.account_page import AccountPage
from page_objects.login_page import LoginPage


@pytest.mark.nondestructive
@pytest.mark.usefixtures("browser", "create_test_user")
class TestAccount:

    @pytest.fixture(autouse=True)
    def setup(self, browser, base_url, create_test_user):
        # Логин пользователя перед каждым тестом
        user_data, access_token = create_test_user
        browser.get(base_url)

        login_page = LoginPage(browser)
        login_page.go_to_login_page()
        login_page.login(user_data["email"], user_data["password"])
        self.account_page = AccountPage(browser)

    def test_go_to_account(self):
        # Тест: Переход по клику на «Личный кабинет»
        self.account_page.go_to_account()
        self.account_page.wait_for_url_contain("account")
        assert "account" in self.account_page.driver.current_url

    def test_go_to_order_history(self):
        #Тест: Переход в раздел «История заказов»
        self.account_page.go_to_account()

        self.account_page.go_to_order_history()
        assert "order-history" in self.account_page.driver.current_url

    def test_logout(self):
        # Тест: Выход из аккаунта
        self.account_page.go_to_account()

        self.account_page.logout()
        self.account_page.go_to_account()
        assert "login" in self.account_page.driver.current_url
