import pytest
import allure

@pytest.mark.nondestructive
class TestOrderFeed:
    @allure.title("При клике на заказ открывается модальное окно с его деталями")
    def test_open_order_details(self, order_feed_page, main_page):
        page = order_feed_page

        page.create_order()
        main_page.close_overlay()
        main_page.close_modal()
        main_page.go_to_order_feed()

        page.open_order_details(order_index=0)

        assert page.is_order_modal_visible(), "Модальное окно с деталями заказа не открылось"

    @allure.title("Заказы из раздела История заказов отображаются на Ленте заказов")
    def test_orders_in_order_feed(self, order_feed_page, main_page):
        page = order_feed_page

        page.create_order()
        main_page.close_overlay()
        main_page.close_modal()

        page.go_to_account()

        page.go_to_order_history()

        orders = page.get_orders()
        assert len(orders) > 0, "Заказы не отображаются в Ленте заказов"

    @allure.title("Счётчик выполненных заказов увеличивается при создании нового заказa")
    def test_completed_counter_increase(self, order_feed_page, main_page):
        page = order_feed_page

        main_page.go_to_order_feed()

        initial_count = page.get_completed_counter()
        main_page.go_to_constructor()

        page.create_order()
        main_page.close_overlay()
        main_page.close_modal()

        main_page.go_to_order_feed()

        new_count = page.get_completed_counter()
        assert new_count > initial_count, f"Счётчик выполненных заказов не увеличился: {new_count} <= {initial_count}"

    @allure.title("Счётчик заказов за сегодня увеличивается при создании нового заказа")
    def test_today_counter_increase(self, order_feed_page, main_page):
        page = order_feed_page

        main_page.go_to_order_feed()

        initial_count = page.get_today_counter()

        main_page.go_to_constructor()

        page.create_order()
        main_page.close_overlay()
        main_page.close_modal()

        main_page.go_to_order_feed()

        new_count = page.get_today_counter()
        assert new_count > initial_count, f"Счётчик заказов за сегодня не увеличился: {new_count} <= {initial_count}"

    @allure.title("Номер нового заказа появляется в разделе В работе")
    def test_order_in_progress(self, order_feed_page, main_page):
        page = order_feed_page

        page.create_order()
        main_page.close_overlay()
        main_page.close_modal()

        main_page.go_to_order_feed()

        in_progress_orders = page.get_in_progress_orders()
        assert len(in_progress_orders) > 0, "Новый заказ не появился в разделе В работе"
