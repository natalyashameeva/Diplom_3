from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Клик по элементу")
    def click_element(self, locator, timeout=10):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Ожидание, что URL содержит подстроку")
    def wait_for_url_contain(self, partial_url, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(partial_url),
            message=f"URL не содержит '{partial_url}' после {timeout} секунд ожидания"
        )

    @allure.step("Открытие заданного URL")
    def open_url(self, url):
        self.driver.get(url)

    @allure.step("Клик по элементу, с возможностью прокрутки к нему")
    def click_element_scroll(self, locator, timeout=10, scroll_into_view=False):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        if scroll_into_view:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

    @allure.step("Ожидание, что URL содержит заданную подстроку")
    def wait_for_url(self, partial_url, timeout=10):
        self.wait.until(
            EC.url_contains(partial_url),
            message=f"URL не содержит '{partial_url}' после {timeout} секунд ожидания"
        )

    @allure.step("Найти элемент на странице")
    def find_element(self, locator, timeout=10):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Получить значение атрибута элемента")
    def get_attribute(self, locator, attribute, timeout=10):
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)

    @allure.step("Проверка видимости элемента")
    def is_element_visible(self, locator, timeout=10):
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except Exception:
            return False

    @allure.step("Ожидание, пока элемент станет кликабельным")
    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            f"Элемент {locator} не стал кликабельным за {timeout} секунд"
        )

    @allure.step("Ожидание, пока элемент исчезнет с экрана")
    def wait_for_element_to_be_invisible(self, locator, timeout=10):
        self.wait.until(
            EC.invisibility_of_element_located(locator),
            f"Элемент {locator} не исчез за {timeout} секунд"
        )

    @allure.step("Ожидание, пока на странице появятся все элементы по заданному локатору")
    def wait_for_elements_to_be_present(self, locator, timeout=10):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator),
            f"Элементы {locator} не загрузились за {timeout} секунд"
        )

    @allure.step("Закрытие модального окна")
    def close_modal(self, modal_locator, close_button_locator):
        close_button = self.wait_for_element_to_be_clickable(close_button_locator)
        close_button.click()
        self.wait_for_element_to_be_invisible(modal_locator)

    @allure.step("Ожидание, пока элемент не станет видимым")
    def wait_for_element_to_be_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            f"Элемент {locator} не стал видимым за {timeout} секунд"
        )

    @allure.step("Очистка поля ввода и ввод текста")
    def clear_and_send_keys(self, locator, text):
        element = self.wait_for_element_to_be_visible(locator)
        element.clear()
        element.send_keys(text)


