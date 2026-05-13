from selenium.webdriver.common.by import By

from pages.base_page import BasePage

import time


class HeaderComponent(BasePage):

    MEAL_PLAN_BUTTON = (
        By.XPATH,
        "//a[contains(@href, 'meal-plan')]"
    )

    SHOPPING_LIST_BUTTON = (
        By.XPATH,
        "//a[contains(@href, 'shopping')]"
    )

    PROFILE_BUTTON = (
        By.XPATH,
        "//div[contains(@class, 'v-avatar') and contains(@class, 'cursor-pointer')]"
    )

    LOGOUT_BUTTON = (
        By.XPATH,
        "//div[contains(text(), 'Выйти')]"
    )

    def open_meal_plan(self):

        self.click(self.MEAL_PLAN_BUTTON)

    def open_shopping_list(self):

        self.click(self.SHOPPING_LIST_BUTTON)

    def open_profile_menu(self):

        self.click(self.PROFILE_BUTTON)

        time.sleep(5)

    def is_user_logged_in(self):

        self.open_profile_menu()

        return self.wait_for_element(
            self.LOGOUT_BUTTON
        ).is_displayed()