from selenium.webdriver.common.by import By
class ForgotPasswordLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    RECOVER_PASSWORD_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    SHOW_PASSWORD_BUTTON = (By.XPATH, "//div[@class='input__icon input__icon-action']")
    PASSWORD_FIELD = (By.XPATH, "//input[@name='Введите новый пароль']")

