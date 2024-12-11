from locators.order_feed_page_locators import OrderFeedPageLocators
from page_objects.base_page import BasePage
import allure
class OrderFeedPage(BasePage):
    @allure.step("Открытие карточки заказа")
    def open_order_details(self, order_index=0):
        self.wait_for_elements_to_be_present(OrderFeedPageLocators.ORDER_ITEM)
        orders = self.driver.find_elements(*OrderFeedPageLocators.ORDER_ITEM)
        if not orders:
            raise ValueError("Заказы не найдены на странице.")
        orders[order_index].click()

    def is_order_modal_visible(self):
        return self.is_element_visible(OrderFeedPageLocators.ORDER_MODAL)

    def go_to_account(self):
        self.click_element(OrderFeedPageLocators.ACCOUNT_TAB)

    @allure.step("Переход в историю заказов")
    def go_to_order_history(self):
        self.click_element(OrderFeedPageLocators.ORDER_HISTORY_TAB)

    def get_completed_counter(self):
        element_text = self.find_element(OrderFeedPageLocators.COMPLETED_COUNTER).text
        return int(element_text.split()[-1])

    def get_today_counter(self):
        element_text = self.find_element(OrderFeedPageLocators.TODAY_COUNTER)
        return int(element_text.split()[-1])

    def get_in_progress_orders(self):
        self.wait_for_elements_to_be_present(OrderFeedPageLocators.IN_PROGRESS_ORDER)
        return self.driver.find_elements(*OrderFeedPageLocators.IN_PROGRESS_ORDER)

    def create_order(self):
        from page_objects.main_page import MainPage
        main_page = MainPage(self.driver)
        main_page.add_ingredient_to_order(ingredient_index=0)
        main_page.place_order()
        assert main_page.is_order_success_modal_visible(), "Модальное окно успешного заказа не появилось"

    def get_orders(self):
        self.wait_for_elements_to_be_present(OrderFeedPageLocators.ORDER_HISTORY_ITEM)
        return self.driver.find_elements(*OrderFeedPageLocators.ORDER_HISTORY_ITEM)

    def get_orders_from_feed(self):
        self.wait_for_elements_to_be_present(OrderFeedPageLocators.ORDER_ITEM)
        return self.driver.find_elements(*OrderFeedPageLocators.ORDER_ITEM)
