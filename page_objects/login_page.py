from locators.login_page_locators import LoginPageLocators
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.main_page_locators import MainPageLocators


class LoginPage:
    """Класс для работы со страницей авторизации"""

    def __init__(self, driver):
        self.driver = driver

    def enter_email(self, email):
        """Ввод email пользователя"""
        # Ожидание, пока поле ввода email не станет видимым
        email_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(LoginPageLocators.EMAIL_FIELD)
        )

        # Очищаем поле и вводим email
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password):
        """Ввод пароля пользователя"""
        password_field = self.driver.find_element(*LoginPageLocators.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """Клик на кнопку входа"""
        login_button = self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        ActionChains(self.driver).move_to_element(login_button).click().perform()

    def login(self, email, password):
        """Объединяет шаги входа в систему"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def go_to_login_page(self):
        """Переходит на страницу логина."""
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")),
            "Кнопка входа в аккаунт не найдена или недоступна"
        )
        login_button.click()

    def wait_for_authorization(self):
        """Ожидает завершения авторизации."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.PLACE_ORDER_BUTTON),
            "Авторизация не завершилась: не появилась кнопка 'Личный кабинет'."
        )