import pytest

@pytest.mark.nondestructive
@pytest.mark.usefixtures("browser")
class TestPasswordRecovery:

    def test_open_recovery_page(self, forgot_password_page):
        # Тест: Переход на страницу восстановления пароля
        # Проверка: страница восстановления пароля открыта
        assert "forgot-password" in forgot_password_page.driver.current_url, \
            "Не удалось перейти на страницу восстановления пароля"

    def test_email_submission(self, forgot_password_page, test_email, reset_password_url):
        # Тест: Ввод почты и отправка запроса на восстановление пароля
        # Вводим email
        forgot_password_page.enter_email(test_email)

        # Кликаем на кнопку "Восстановить"
        forgot_password_page.click_recover_password()

        # Ожидание перехода на страницу ввода нового пароля
        forgot_password_page.wait_for_reset_password_url(reset_password_url)

        # Проверка: страницы ввода нового пароля
        assert reset_password_url in forgot_password_page.driver.current_url

    def test_toggle_show_password(self, forgot_password_page, test_email, reset_password_url):
        # Тест: Кнопка показать/скрыть делает поле пароля активным
        # Вводим email и кликаем на кнопку "Восстановить"
        forgot_password_page.enter_email(test_email)
        forgot_password_page.click_recover_password()

        # Ожидание перехода на страницу ввода нового пароля
        forgot_password_page.wait_for_url_contains(reset_password_url)

        # Тоггл кнопки показать/скрыть пароль
        forgot_password_page.toggle_password_visibility()

        # Проверка: поле пароля подсвечивается, указывая, что оно активно
        assert forgot_password_page.is_password_field_highlighted(), \
            "Поле пароля не подсвечено при нажатии кнопки 'показать пароль'"
