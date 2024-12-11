from locators.main_page_locators import MainPageLocators
from page_objects.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
import allure
class MainPage(BasePage):
    @allure.step("Переход на вкладку конструктора")
    def go_to_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_TAB)

    @allure.step("Переход на вкладку ленты заказов")
    def go_to_order_feed(self):
        self.click_element(MainPageLocators.ORDER_FEED_TAB)

    @allure.step("Открытие модального окна ингредиента по индексу")
    def open_ingredient_modal(self, index=0):
        ingredients = self.wait_for_elements_to_be_present(MainPageLocators.INGREDIENT_ITEM)
        ingredients[index].click()

    @allure.step("Закрытие модального окна на главной странице")
    def close_modal(self, modal_locator=MainPageLocators.MODAL, close_button_locator=MainPageLocators.CLOSE_BUTTON):
        super().close_modal(modal_locator, close_button_locator)

    @allure.step("Ожидание загрузки всех ингредиентов")
    def wait_for_ingredients_to_load(self):
        self.wait_for_elements_to_be_present(MainPageLocators.INGREDIENT_ITEM)

    @allure.step("Добавление ингредиента в заказ")
    def add_ingredient_to_order(self, ingredient_index=0):
        self.wait_for_ingredients_to_load()
        ingredients = self.wait_for_elements_to_be_present(MainPageLocators.INGREDIENT_ITEM)
        ingredient = ingredients[ingredient_index]
        order_area = self.find_element(MainPageLocators.ORDER_AREA)

        action = ActionChains(self.driver)
        action.drag_and_drop(ingredient, order_area).perform()

    @allure.step("Проверка обновления счетчика ингредиента")
    def is_ingredient_counter_updated(self, ingredient_index=0):
        counters = self.wait_for_elements_to_be_present(MainPageLocators.INGREDIENT_COUNTER)
        return int(counters[ingredient_index].text) > 0

    @allure.step("Проверка, что модальное окно успешного заказа отображается")
    def is_order_success_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ORDER_SUCCESS_MODAL)

    @allure.step("Оформление заказа")
    def place_order(self):
        self.click_element(MainPageLocators.PLACE_ORDER_BUTTON)

    @allure.step("Закрытие оверлея")
    def close_overlay(self):
        try:
            overlay = self.wait_for_element_to_be_clickable(MainPageLocators.OVERLAY)
            overlay.click()
        except Exception as e:
            print(f"Оверлей не найден или недоступен: {e}")
