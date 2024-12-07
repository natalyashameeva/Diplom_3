from selenium.webdriver.common.by import By

class MainPageLocators:
    CONSTRUCTOR_TAB = (By.XPATH, "//a[@href='/']")
    ORDER_FEED_TAB = (By.XPATH, "//a[@href='/feed']")
    INGREDIENT_ITEM = (By.CLASS_NAME, "BurgerIngredient_ingredient__text__yp3dH")
    INGREDIENT_COUNTER = (By.CLASS_NAME, "counter_counter__num__3nue1")
    MODAL = (By.CLASS_NAME, "Modal_modal__container__Wo2l_")
    CLOSE_BUTTON = (By.CLASS_NAME, "Modal_modal__close_modified__3V5XS")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_SUCCESS_MODAL = (By.CLASS_NAME, "Modal_modal__container__Wo2l_")
    ORDER_AREA = (By.CLASS_NAME, "BurgerConstructor_basket__list__l9dp_")
    OVERLAY = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")

