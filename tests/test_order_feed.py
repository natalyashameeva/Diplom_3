import pytest
from page_objects.order_feed_page import OrderFeedPage
from locators.order_feed_page_locators import OrderFeedPageLocators
from page_objects.login_page import LoginPage
from page_objects.main_page import MainPage


@pytest.mark.nondestructive
@pytest.mark.usefixtures("create_test_user", "browser", "base_url")
class TestOrderFeed:

    @pytest.fixture(autouse=True)
    def setup(self, browser, base_url, create_test_user):
        #Логин пользователя перед каждым тестом
        user_data, access_token = create_test_user
        browser.get(base_url)

        login_page = LoginPage(browser)
        login_page.go_to_login_page()
        login_page.login(user_data["email"], user_data["password"])
        login_page.wait_for_authorization()
        self.order_feed_page = OrderFeedPage(browser)

    def test_open_order_details(self, browser, base_url):
        #Проверяет, что при клике на заказ открывается модальное окно с его деталями
        browser.get(base_url)
        page = OrderFeedPage(browser)

        # Создаем заказ перед тестом
        page.create_order()
        main_page = MainPage(browser)
        main_page.close_overlay()
        main_page.close_modal()
        main_page.go_to_order_feed()

        # Открываем заказ
        page.open_order_details(order_index=0)

        # Проверяем, что модальное окно с деталями заказа открылось
        assert page.is_order_modal_visible(), "Модальное окно с деталями заказа не открылось"

    def test_orders_in_order_feed(self, browser, base_url):
        #Проверяет, что заказы из раздела История заказов отображаются на Ленте заказов.
        browser.get(base_url)
        page = OrderFeedPage(browser)
        # Создаем заказ перед тестом
        page.create_order()
        main_page = MainPage(browser)
        main_page.close_overlay()
        main_page.close_modal()

        # Переходим в раздел "Личный кабинет"
        page.go_to_account()

        # Переходим в раздел "История заказов"
        page.go_to_order_history()

        # Проверяем, что заказы отображаются в ленте заказов
        orders = page.get_orders()
        assert len(orders) > 0, "Заказы не отображаются в Ленте заказов"

        # Получаем список заказов из истории заказов
        history_orders = page.browser.find_elements(*OrderFeedPageLocators.ORDER_HISTORY_ITEM)

        # Сохраняем идентификаторы заказов из "Истории заказов"
        history_order_ids = [order.get_attribute("data-order-id") for order in history_orders]

        # Переходим в раздел "Лента заказов"
        main_page.go_to_order_feed()

        # Проверяем, что заказы из истории отображаются в ленте заказов
        feed_orders = page.get_orders_from_feed()
        feed_order_ids = [order.get_attribute("data-order-id") for order in feed_orders]

        # Сравниваем списки идентификаторов заказов
        for order_id in history_order_ids:
            assert order_id in feed_order_ids, f"Заказ с ID {order_id} отсутствует в Ленте заказов"

    def test_completed_counter_increase(self, browser, base_url):
        #Проверяет, что счётчик выполненных заказов увеличивается при создании нового заказa
        browser.get(base_url)
        page = OrderFeedPage(browser)
        main_page = MainPage(browser)
        # Переходим в раздел "Лента заказов"
        main_page.go_to_order_feed()

        initial_count = page.get_completed_counter()
        # Переходим в раздел "Конструктор"
        main_page.go_to_constructor()

        # Создаём новый заказ
        page.create_order()
        main_page.close_overlay()
        main_page.close_modal()
        # Переходим в раздел "Лента заказов"
        main_page.go_to_order_feed()

        # Проверяем, что счётчик увеличился
        new_count = page.get_completed_counter()
        assert new_count > initial_count, f"Счётчик выполненных заказов не увеличился: {new_count} <= {initial_count}"

    def test_today_counter_increase(self, browser, base_url):
        #Проверяет, что счётчик заказов за сегодня увеличивается при создании нового заказа
        browser.get(base_url)
        page = OrderFeedPage(browser)
        main_page = MainPage(browser)
        # Переходим в раздел "Лента заказов"
        main_page.go_to_order_feed()

        initial_count = page.get_today_counter

        # Переходим в раздел "Конструктор"
        main_page.go_to_constructor()

        # Создаём новый заказ
        page.create_order()
        main_page.close_overlay()
        main_page.close_modal()
        # Переходим в раздел "Лента заказов"
        main_page.go_to_order_feed()
        # Проверяем, что счётчик увеличился
        new_count = page.get_today_counter
        assert new_count > initial_count, f"Счётчик заказов за сегодня не увеличился: {new_count} <= {initial_count}"

    def test_order_in_progress(self, browser, base_url):
        # Проверяет, что номер нового заказа появляется в разделе В работе
        browser.get(base_url)
        page = OrderFeedPage(browser)

        # Создаём новый заказ
        page.create_order()
        main_page = MainPage(browser)
        main_page.close_overlay()
        main_page.close_modal()
        # Переходим в раздел "Лента заказов"
        main_page.go_to_order_feed()

        # Проверяем, что заказ появился в статусе "В работе"
        in_progress_orders = page.get_in_progress_orders()
        assert len(in_progress_orders) > 0, "Новый заказ не появился в разделе В работе"
