from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.order_feed_page_locators import OrderFeedPageLocators
from page_objects.main_page import MainPage


class OrderFeedPage:
    def __init__(self, browser):
        self.browser = browser

    """Кликает по заказу, чтобы открыть модальное окно с его деталями"""
    def open_order_details(self, order_index=0):

        # Ожидаем, что хотя бы один заказ будет видим на странице
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_all_elements_located(OrderFeedPageLocators.ORDER_ITEM)
        )

        # Получаем все элементы заказов
        orders = self.browser.find_elements(*OrderFeedPageLocators.ORDER_ITEM)

        # Проверяем, что заказы действительно есть на странице
        if not orders:
            raise ValueError("Заказы не найдены на странице.")

        # Кликаем на заказ по индексу
        orders[order_index].click()

    def is_order_modal_visible(self):
        """Проверяет, что модальное окно с деталями заказа открыто."""
        try:
            modal = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_MODAL)
            )
            return modal.is_displayed()
        except:
            return False

    def go_to_account(self):
        """Переходит на вкладку «Личный кабинет»."""
        account_tab = self.browser.find_element(*OrderFeedPageLocators.ACCOUNT_TAB)
        account_tab.click()

    def go_to_order_history(self):
        """Переходит на вкладку «История заказов»."""
        history_tab = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(OrderFeedPageLocators.ORDER_HISTORY_TAB)
        )

        history_tab.click()

    def get_completed_counter(self):
        """Возвращает количество выполненных заказов за всё время."""
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(OrderFeedPageLocators.COMPLETED_COUNTER)
        )
        return int(self.browser.find_element(*OrderFeedPageLocators.COMPLETED_COUNTER).text.split()[-1])

    @property
    def get_today_counter(self):
        """Возвращает количество выполненных заказов за сегодня."""
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(OrderFeedPageLocators.TODAY_COUNTER)
        )
        element = self.browser.find_element(*OrderFeedPageLocators.TODAY_COUNTER)
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
        return int(element.text.split()[-1])

    def get_in_progress_orders(self):
        """Возвращает все заказы в статусе «В работе»."""
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(OrderFeedPageLocators.IN_PROGRESS_ORDER)
        )
        return self.browser.find_elements(*OrderFeedPageLocators.IN_PROGRESS_ORDER)

    def create_order(self):
        """Создаёт заказ, добавляя ингредиенты и оформляя заказ."""
        # Переход на страницу с заказами, если необходимо
        main_page = MainPage(self.browser)

        # Добавить ингредиент в заказ (например, первый ингредиент)
        main_page.add_ingredient_to_order(ingredient_index=0)

        # Оформить заказ
        main_page.place_order()

        # Подтвердить, что заказ был успешно оформлен
        assert main_page.is_order_success_modal_visible(), "Модальное окно успешного заказа не появилось"

    def wait_for_orders_to_load(self, timeout=10):
        """
        Ожидает, что заказы появятся в истории заказов.
        """
        WebDriverWait(self.browser, timeout).until(
            EC.presence_of_all_elements_located(OrderFeedPageLocators.ORDER_HISTORY_ITEM),
            message="Заказы не появились в Ленте заказов"
        )

    def wait_for_feed_to_load(self, timeout=10):
        """
        Ожидает, что заказы появятся в Ленте заказов.
        """
        WebDriverWait(self.browser, timeout).until(
            EC.presence_of_all_elements_located(OrderFeedPageLocators.ORDER_ITEM),
            message="Заказы не появились в Ленте заказов"
        )

    def get_orders(self):
        """
        Возвращает список элементов заказов из Истории заказов.
        """
        self.wait_for_orders_to_load()
        return self.browser.find_elements(*OrderFeedPageLocators.ORDER_HISTORY_ITEM)

    def get_orders_from_feed(self):
        """
        Возвращает список элементов заказов из Ленты заказов.
        """
        self.wait_for_feed_to_load()
        return self.browser.find_elements(*OrderFeedPageLocators.ORDER_ITEM)
