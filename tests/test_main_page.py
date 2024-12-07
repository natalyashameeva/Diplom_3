import pytest
from page_objects.main_page import MainPage
from page_objects.login_page import LoginPage
from locators.main_page_locators import MainPageLocators

@pytest.mark.nondestructive
class TestMainPage:
    def test_navigation_to_constructor(self, browser, forgot_password_url, base_url):
        # Проверяет переход по клику на «Конструктор».
        browser.get(forgot_password_url)
        page = MainPage(browser)
        page.go_to_constructor()
        current_url = browser.current_url.rstrip("/")
        expected_url = base_url.rstrip("/")
        assert current_url == expected_url, f"Ожидаемый URL: {expected_url}, но был: {current_url}"

    def test_navigation_to_order_feed(self, browser, base_url):
        # Проверяет переход по клику на «Лента заказов».
        browser.get(base_url)
        page = MainPage(browser)
        page.go_to_order_feed()
        assert "feed" in browser.current_url, "Не удалось перейти на страницу ленты заказов"

    def test_ingredient_modal_open_close(self, browser, base_url):
        # Проверяет открытие и закрытие модального окна ингредиента.
        browser.get(base_url)
        page = MainPage(browser)
        page.open_ingredient_modal()
        assert page.is_element_visible(MainPageLocators.MODAL), "Модальное окно не появилось"
        page.close_modal()
        assert not page.is_element_visible(MainPageLocators.MODAL), "Модальное окно не закрылось"

    def test_add_ingredient_to_order(self, browser, base_url):
        # Проверяет добавление ингредиента в заказ.
        browser.get(base_url)
        page = MainPage(browser)
        # Добавить первый ингредиент в заказ
        page.add_ingredient_to_order(ingredient_index=0)

        # Проверить, что счетчик у ингредиента увеличился
        assert page.is_ingredient_counter_updated(ingredient_index=0), "Счетчик ингредиента не увеличился"

    @pytest.fixture
    def setup(self, browser, base_url, create_test_user):
        # Логин пользователя перед тестом.
        user_data, access_token = create_test_user
        browser.get(base_url)

        login_page = LoginPage(browser)
        login_page.go_to_login_page()
        login_page.login(user_data["email"], user_data["password"])
        self.main_page = MainPage(browser)

    @pytest.mark.usefixtures("setup")
    def test_place_order_logged_in(self):
        # Проверяет возможность оформления заказа залогиненным пользователем.
        # Добавить ингредиент в заказ
        self.main_page.add_ingredient_to_order(ingredient_index=0)

        # Проверить оформление заказа
        self.main_page.place_order()
        assert self.main_page.is_order_success_modal_visible(), "Модальное окно успешного заказа не появилось"





