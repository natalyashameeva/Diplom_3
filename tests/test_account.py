import pytest
import allure

@pytest.mark.nondestructive
@pytest.mark.usefixtures("driver", "create_test_user")
class TestAccount:
    @allure.title("Переход по клику на «Личный кабинет»")
    def test_go_to_account(self, account_page):
        account_page.go_to_account()
        account_page.wait_for_url_contain("account")
        assert "account" in account_page.driver.current_url

    @allure.title("Переход в раздел «История заказов»")
    def test_go_to_order_history(self, account_page):
        account_page.go_to_account()
        account_page.go_to_order_history()
        assert "order-history" in account_page.driver.current_url

    @allure.title("Выход из аккаунта")
    def test_logout(self, account_page):
        account_page.go_to_account()
        account_page.logout()
        account_page.go_to_account()
        assert "login" in account_page.driver.current_url

