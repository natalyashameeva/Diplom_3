from locators.main_page_locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class MainPage:
    def __init__(self, browser):
        self.browser = browser

    def click(self, locator):
        self.browser.find_element(*locator).click()

    def get_element(self, locator):
        return self.browser.find_element(*locator)

    def is_element_visible(self, locator):
        return self.get_element(locator).is_displayed()

    def go_to_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_TAB)

    def go_to_order_feed(self):
        self.click(MainPageLocators.ORDER_FEED_TAB)

    def open_ingredient_modal(self, index=0):
        ingredients = self.browser.find_elements(*MainPageLocators.INGREDIENT_ITEM)
        ingredients[index].click()

    def close_modal(self):
        close_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(MainPageLocators.CLOSE_BUTTON),
            "Кнопка закрытия модального окна недоступна."
        )
        close_button.click()
        WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located(MainPageLocators.MODAL),
            "Модальное окно не закрылось."
        )

    def wait_for_ingredients_to_load(self, timeout=10):
        """Ожидает загрузки ингредиентов на странице."""
        WebDriverWait(self.browser, timeout).until(
            EC.presence_of_all_elements_located(MainPageLocators.INGREDIENT_ITEM),
            "Ингредиенты не появились на странице"
        )
    def add_ingredient_to_order(self, ingredient_index=0):
        """Добавляет ингредиент в заказ методом перетаскивания."""
        # Ожидание загрузки ингредиентов
        self.wait_for_ingredients_to_load()

        # Найти элемент ингредиента
        ingredients = self.browser.find_elements(*MainPageLocators.INGREDIENT_ITEM)
        if not ingredients:
            raise ValueError("Ингредиенты не найдены на странице.")
        ingredient = ingredients[ingredient_index]

        # Найти целевую область корзины
        order_area = self.browser.find_element(*MainPageLocators.ORDER_AREA)

        # Перетаскивание ингредиента в область заказа
        action = ActionChains(self.browser)
        action.drag_and_drop(ingredient, order_area).perform()

    def is_ingredient_counter_updated(self, ingredient_index=0):
        """Проверяет, увеличился ли счетчик у указанного ингредиента."""
        counters = self.browser.find_elements(*MainPageLocators.INGREDIENT_COUNTER)
        if not counters or len(counters) <= ingredient_index:
            return False
        return int(counters[ingredient_index].text) > 0

    def is_order_success_modal_visible(self, timeout=10):
        """Проверяет, отображается ли модальное окно успешного заказа."""
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located(MainPageLocators.ORDER_SUCCESS_MODAL)
            )
            return True
        except TimeoutError:
            return False


    def place_order(self):
        place_order_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(MainPageLocators.PLACE_ORDER_BUTTON),
            "Кнопка 'Оформить заказ' недоступна."
        )
        place_order_button.click()

    def close_overlay(self):
        """Закрывает оверлей."""
        try:
            # Попытка кликнуть по оверлею
            overlay = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(MainPageLocators.OVERLAY)
            )
            overlay.click()
        except Exception as e:
            print(f"Оверлей не найден или недоступен: {e}")

