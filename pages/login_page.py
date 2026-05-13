from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME_INPUT = (By.ID, "id_login")

    PASSWORD_INPUT = (By.ID, "id_password")

    LOGIN_BUTTON = (
        By.XPATH,
        "//button[contains(text(), 'Войти')]"
    )

    def login(self, username, password):

        self.type(self.USERNAME_INPUT, username)

        self.type(self.PASSWORD_INPUT, password)

        self.click(self.LOGIN_BUTTON)