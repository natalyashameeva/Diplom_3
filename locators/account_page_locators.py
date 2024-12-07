from selenium.webdriver.common.by import By

class AccountLocators:
    ACCOUNT_BUTTON = (By.CSS_SELECTOR, "a[href='/account']")
    ORDER_HISTORY_BUTTON = (By.CSS_SELECTOR, "a[href='/account/order-history']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, ".Account_button__14Yp3")

