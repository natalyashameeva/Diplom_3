from locators.login_page_locators import LoginPageLocators
from locators.main_page_locators import MainPageLocators
from page_objects.base_page import BasePage
import allure
class LoginPage(BasePage):

    @allure.step("Ввод email пользователя")
    def enter_email(self, email):
        self.clear_and_send_keys(LoginPageLocators.EMAIL_FIELD, email)

    @allure.step("Ввод пароля пользователя")
    def enter_password(self, password):
        self.clear_and_send_keys(LoginPageLocators.PASSWORD_FIELD, password)

    @allure.step("Клик на кнопку входа")
    def click_login(self):
        self.click_element(LoginPageLocators.LOGIN_BUTTON)

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def wait_for_authorization(self):
        self.wait_for_element_to_be_visible(MainPageLocators.PLACE_ORDER_BUTTON)

    @allure.step("Переход на страницу логина")
    def go_to_login_page(self):
        self.click_element(LoginPageLocators.GO_LOGIN_BUTTON)