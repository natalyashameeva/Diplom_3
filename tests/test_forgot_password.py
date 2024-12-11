import pytest
import allure

@pytest.mark.nondestructive
@pytest.mark.usefixtures("driver")
class TestPasswordRecovery:
    @allure.title("Переход на страницу восстановления пароля")
    def test_open_recovery_page(self, forgot_password_page):
        assert "forgot-password" in forgot_password_page.driver.current_url, \
            "Не удалось перейти на страницу восстановления пароля"

    @allure.title("Ввод почты и отправка запроса на восстановление пароля")
    def test_email_submission(self, forgot_password_page, test_email, reset_password_url):

        forgot_password_page.enter_email(test_email)

        forgot_password_page.click_recover_password()

        forgot_password_page.wait_for_url(reset_password_url)

        assert reset_password_url in forgot_password_page.driver.current_url

    @allure.title("Кнопка показать/скрыть делает поле пароля активным")
    def test_toggle_show_password(self, forgot_password_page, test_email, reset_password_url):

        forgot_password_page.enter_email(test_email)
        forgot_password_page.click_recover_password()

        forgot_password_page.wait_for_url(reset_password_url)

        forgot_password_page.toggle_password_visibility()

        assert forgot_password_page.is_password_field_highlighted(), \
            "Поле пароля не подсвечено при нажатии кнопки 'показать пароль'"
