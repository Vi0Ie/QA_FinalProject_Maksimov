from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import random
import time

from pages.base_page import BasePage


class MealPlanPage(BasePage):

    CALENDAR_DAYS = (
        By.CSS_SELECTOR,
        "div.cv-day"
    )

    RECIPE_FIELD = (
        By.XPATH,
        "(//input[contains(@class,'multiselect-search')])[1]"
    )

    CREATE_BUTTON = (
        By.XPATH,
        "//span[contains(text(), 'Создать')]"
    )


    DATE_CONTROLS = (
        By.XPATH,
        "(//div[contains(@class,'v-btn-group')])[1]//button"
    )

    TIME_INPUT = (
        By.XPATH,
        "//label[contains(text(),'Время')]/following::input[1]"
    )

    DATE_RANGE_BUTTONS = (
        By.CSS_SELECTOR,
        ".v-btn-group button"
    )

    MEAL_TYPE_FIELD = (
        By.XPATH,
        "(//input[contains(@class,'multiselect-search')])[2]"
    )

    SERVINGS_FIELD = (
        By.ID,
        "input-v-0-23"
    )

    SERVINGS_DECREMENT_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-testid='decrement']"
    )

    SERVINGS_INCREMENT_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-testid='increment']"
    )

    SHOPPING_LIST_CHECKBOX = (
        By.ID,
        "checkbox-v-0-33"
    )

    NOTES_FIELD = (
        By.ID,
        "input-v-0-28"
    )

    CREATE_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Создать')]"
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Сохранить')]"
    )

    DELETE_BUTTON = (
        By.XPATH,
        "(//button[contains(., 'Удалить')])[1]"
    )

    CONFIRM_DELETE_BUTTON = (
        By.XPATH,
        "(//button[contains(., 'Удалить')])[2]"
    )

    RECIPE_LINK = (
        By.CSS_SELECTOR,
        "a[href*='/view/recipe/']"
    )

    SHOPPING_LIST_TAB = (
        By.XPATH,
        "//button[@value='shopping']"
    )

    SHOPPING_LIST_ITEMS = (
        By.XPATH,
        "//div[contains(@class, 'shopping')]"
    )

    SHOPPING_LIST_ROWS = (
        By.XPATH,
        "//div[contains(@class, 'v-list-item')]"
    )

    def open_meal_plan_page(self, base_url):
        self.open(
            f"{base_url}/mealplan"
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div.cv-day"
                )
            )
        )

    def click_calendar_day(self):
        days = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".cv-day"
        )

        random_index = random.randint(0, len(days) - 1)

        # первый клик
        days[random_index].click()

        # ждем overlay/loading
        time.sleep(3)

        # ждем пока overlay исчезнет
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".v-overlay__scrim")
            )
        )

        # заново ищем дни после перерисовки
        new_days = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".cv-day"
        )

        # второй клик по обновленному элементу
        new_days[random_index].click()

        time.sleep(2)

    def select_recipe(self, recipe_name):

        recipe_field = self.wait.until(
            EC.visibility_of_element_located(
                self.RECIPE_FIELD
            )
        )

        recipe_field.click()

        recipe_field.clear()

        recipe_field.send_keys(recipe_name)

        recipe_option = (
            By.XPATH,
            f"//*[contains(text(), '{recipe_name}')]"
        )

        recipe_element = self.wait.until(
            EC.presence_of_element_located(
                recipe_option
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            recipe_element
        )

        time.sleep(1)

        try:
            recipe_element.click()

        except Exception:

            self.driver.execute_script(
                "arguments[0].click();",
                recipe_element
            )


    def increase_date_range(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.DATE_CONTROLS
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            buttons[3]
        )

    def decrease_date_range(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.DATE_CONTROLS
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            buttons[0]
        )

    def previous_date_range(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.DATE_CONTROLS
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            buttons[1]
        )

    def next_date_range(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.DATE_CONTROLS
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            buttons[2]
        )
    def fill_time(self, time_value):
        time_input = self.wait.until(
            EC.element_to_be_clickable(
                self.TIME_INPUT
            )
        )

        self.driver.execute_script(
            "arguments[0].removeAttribute('readonly')",
            time_input
        )

        time_input.clear()

        time_input.send_keys(time_value)

    def select_meal_type(self, meal_type):
        field = self.wait.until(
            EC.element_to_be_clickable(
                self.MEAL_TYPE_FIELD
            )
        )

        field.click()

        field.send_keys(meal_type)

        option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//li[contains(., '{meal_type}')]"
                )
            )
        )

        option.click()

    def set_servings(self, value):
        field = self.wait.until(
            EC.element_to_be_clickable(
                self.SERVINGS_FIELD
            )
        )

        field.clear()

        field.send_keys(str(value))

    def increase_servings(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.SERVINGS_INCREMENT_BUTTON
            )
        ).click()

    def decrease_servings(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.SERVINGS_DECREMENT_BUTTON
            )
        ).click()

    def set_add_to_shopping_list(self, enabled=True):
        checkbox = self.wait.until(
            EC.presence_of_element_located(
                self.SHOPPING_LIST_CHECKBOX
            )
        )

        is_checked = checkbox.is_selected()

        if enabled != is_checked:
            checkbox.click()

    def enter_notes(self, text):
        notes = self.wait.until(
            EC.element_to_be_clickable(
                self.NOTES_FIELD
            )
        )

        notes.clear()

        notes.send_keys(text)

    def create_meal_plan(self):

        create_button = self.wait.until(
            EC.presence_of_element_located(
                self.CREATE_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            create_button
        )

        self.wait.until(
            EC.presence_of_element_located(
                self.SAVE_BUTTON
            )
        )

    def is_create_successful(self):

        return self.wait.until(
            EC.visibility_of_element_located(
                self.SAVE_BUTTON
            )
        )

    def delete_meal_plan(self):

        delete_button = self.wait.until(
            EC.element_to_be_clickable(
                self.DELETE_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            delete_button
        )

        confirm_delete = self.wait.until(
            EC.visibility_of_element_located(
                self.CONFIRM_DELETE_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            confirm_delete
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            confirm_delete
        )

        self.wait.until(
            EC.invisibility_of_element_located(
                self.CONFIRM_DELETE_BUTTON
            )
        )

    def refresh_page(self):

        self.driver.refresh()

    def open_created_meal_plan(self, recipe_name):

        # первый поиск и клик
        recipe_plan = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//*[contains(text(), '{recipe_name}')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            recipe_plan
        )

        time.sleep(2)

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".v-overlay__scrim")
            )
        )

        # повторно ищем элемент после перерисовки
        recipe_plan = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//*[contains(text(), '{recipe_name}')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            recipe_plan
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            recipe_plan
        )

        time.sleep(2)

    def get_notes_value(self):

        notes = self.wait.until(
            EC.visibility_of_element_located(
                self.NOTES_FIELD
            )
        )

        return notes.get_attribute("value")

    def get_servings_value(self):

        servings = self.wait.until(
            EC.visibility_of_element_located(
                self.SERVINGS_FIELD
            )
        )

        return servings.get_attribute("value")

    def open_recipe_from_meal_plan(self):

        recipe_image = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "a[href*='/recipe/'] img"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            recipe_image
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].closest('a').click();",
            recipe_image
        )

        time.sleep(2)

    def is_meal_plan_deleted(self, recipe_name):

        plans = self.driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'flex-column') and contains(., '{recipe_name}')]"
        )

        return len(plans) == 0

    def get_meal_plan_id(self):

        current_url = self.driver.current_url

        return current_url.rstrip("/").split("/")[-1]

    def is_add_to_shopping_list_enabled(self):

        checkbox = self.wait.until(
            EC.presence_of_element_located(
                self.SHOPPING_LIST_CHECKBOX
            )
        )

        print(
            checkbox.get_attribute("outerHTML")
        )

    def is_shopping_list_not_empty(self):

        items = self.driver.find_elements(
            *self.SHOPPING_LIST_ROWS
        )

        return len(items) > 0

    def open_shopping_list_tab(self):

        button = self.wait.until(
            EC.element_to_be_clickable(
                self.SHOPPING_LIST_TAB
            )
        )

        button.click()