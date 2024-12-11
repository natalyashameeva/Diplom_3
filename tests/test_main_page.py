import pytest
import allure
from page_objects.main_page import MainPage
from locators.main_page_locators import MainPageLocators
from tests.conftest import BASE_URL


@pytest.mark.nondestructive
class TestMainPage:
    @allure.title("Переход по клику на «Конструктор»")
    def test_navigation_to_constructor(self, driver, forgot_password_url):

        driver.get(forgot_password_url)
        page = MainPage(driver)
        page.go_to_constructor()
        current_url = driver.current_url.rstrip("/")
        expected_url = BASE_URL.rstrip("/")
        assert current_url == expected_url, f"Ожидаемый URL: {expected_url}, но был: {current_url}"

    @allure.title("Переход по клику на «Лента заказов»")
    def test_navigation_to_order_feed(self, driver):

        driver.get(BASE_URL)
        page = MainPage(driver)
        page.go_to_order_feed()
        assert "feed" in driver.current_url, "Не удалось перейти на страницу ленты заказов"

    @allure.title("Открытие и закрытие модального окна ингредиента")
    def test_ingredient_modal_open_close(self, driver):

        driver.get(BASE_URL)
        page = MainPage(driver)
        page.open_ingredient_modal()
        assert page.is_element_visible(MainPageLocators.MODAL), "Модальное окно не появилось"
        page.close_modal()
        assert not page.is_element_visible(MainPageLocators.MODAL), "Модальное окно не закрылось"

    @allure.title("Добавление ингредиента в заказ")
    def test_add_ingredient_to_order(self, driver):
        driver.get(BASE_URL)
        page = MainPage(driver)
        page.add_ingredient_to_order(ingredient_index=0)

        assert page.is_ingredient_counter_updated(ingredient_index=0), "Счетчик ингредиента не увеличился"

    @allure.title("Возможность оформления заказа залогиненным пользователем")
    def test_place_order_logged_in(self, main_page):
        main_page.add_ingredient_to_order(ingredient_index=0)

        main_page.place_order()
        assert main_page.is_order_success_modal_visible(), "Модальное окно успешного заказа не появилось"


