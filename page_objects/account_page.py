from locators.account_page_locators import AccountLocators
from page_objects.base_page import BasePage
import allure

class AccountPage(BasePage):
    @allure.step("Переход на страницу личного кабинета")
    def go_to_account(self):
        self.click_element(AccountLocators.ACCOUNT_BUTTON)

    @allure.step("Переход в раздел 'История заказов'")
    def go_to_order_history(self):
        self.click_element(AccountLocators.ORDER_HISTORY_BUTTON)

    @allure.step("Выход из аккаунта")
    def logout(self):
        self.click_element(AccountLocators.LOGOUT_BUTTON)
