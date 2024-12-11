from locators.forgot_password_locators import ForgotPasswordLocators
from page_objects.base_page import BasePage
import allure
class ForgotPasswordPage(BasePage):
    @allure.step("Открыть страницу восстановления пароля")
    def open_recovery_page(self):
        self.open_url("https://stellarburgers.nomoreparties.site/forgot-password")

    @allure.step("Ввод email для восстановления пароля")
    def enter_email(self, email):
        email_input = self.find_element(ForgotPasswordLocators.EMAIL_INPUT)
        email_input.send_keys(email)

    @allure.step("Нажать на кнопку восстановления пароля")
    def click_recover_password(self):
        self.click_element_scroll(ForgotPasswordLocators.RECOVER_PASSWORD_BUTTON, scroll_into_view=True)

    @allure.step("Клик по кнопке показать/скрыть пароль")
    def toggle_password_visibility(self):
        self.click_element(ForgotPasswordLocators.SHOW_PASSWORD_BUTTON)

    @allure.step("Проверка, что поле пароля активно (подсвечено)")
    def is_password_field_highlighted(self):
        return self.get_attribute(ForgotPasswordLocators.PASSWORD_FIELD, "type") == "text"
