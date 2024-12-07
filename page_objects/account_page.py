from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.account_page_locators import AccountLocators


class AccountPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_account(self):
        """Переход на страницу личного кабинета."""
        account_button = self.wait.until(
            EC.element_to_be_clickable(AccountLocators.ACCOUNT_BUTTON)
        )
        account_button.click()

    # Ожидание, что URL содержит подстроку
    def wait_for_url_contain(self, partial_url, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(partial_url),
            message=f"URL не содержит '{partial_url}' после {timeout} секунд ожидания"
        )

    def go_to_order_history(self):
        """Переход в раздел 'История заказов'."""
        order_history_button = self.wait.until(
            EC.element_to_be_clickable(AccountLocators.ORDER_HISTORY_BUTTON)
        )
        order_history_button.click()


    def logout(self):
        """Выход из аккаунта."""
        logout_button = self.wait.until(
            EC.element_to_be_clickable(AccountLocators.LOGOUT_BUTTON)
        )
        logout_button.click()


