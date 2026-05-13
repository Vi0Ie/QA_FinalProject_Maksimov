from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ShoppingListPage(BasePage):

    SHOPPING_ITEMS = (
        By.CLASS_NAME,
        "shopping-list-entry"
    )

    def open_shopping_list(self, base_url):

        self.open(f"{base_url}/shopping")