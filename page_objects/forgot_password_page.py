from locators.forgot_password_locators import ForgotPasswordLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ForgotPasswordPage:
    def __init__(self, driver):
        self.driver = driver


    def open_recovery_page(self):
        """Открыть страницу восстановления пароля"""
        self.driver.get("https://stellarburgers.nomoreparties.site/forgot-password")


    def enter_email(self, email):
        """Ввод email для восстановления пароля"""
        email_input = self.driver.find_element(*ForgotPasswordLocators.EMAIL_INPUT)
        email_input.send_keys(email)

    def click_recover_password(self):
        recover_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ForgotPasswordLocators.RECOVER_PASSWORD_BUTTON)
        )
        # Прокручиваем к кнопке
        self.driver.execute_script("arguments[0].scrollIntoView();", recover_button)
        recover_button.click()


    def toggle_password_visibility(self):
        """Клик по кнопке показать/скрыть пароль для активации поля"""
        show_button = self.driver.find_element(*ForgotPasswordLocators.SHOW_PASSWORD_BUTTON)
        show_button.click()
    def is_password_field_highlighted(self):
        """Проверка, что поле пароля активно (подсвечено)"""
        password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(ForgotPasswordLocators.PASSWORD_FIELD)
            )
        return password_field.get_attribute("type") == "text"

    def wait_for_reset_password_url(self, reset_password_url, timeout=10):
        """Ожидает, что URL изменится на URL страницы сброса пароля."""
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(reset_password_url),
            message=f"URL не содержит {reset_password_url} после {timeout} секунд ожидания"
        )

    def wait_for_url_contains(self, partial_url, timeout=20):
        """Ожидает, что URL содержит заданную подстроку."""
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(partial_url),
            message=f"URL не содержит '{partial_url}' после {timeout} секунд ожидания"
        )