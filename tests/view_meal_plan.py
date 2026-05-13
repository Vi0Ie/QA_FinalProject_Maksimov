import os
import random
import time

import allure

from dotenv import load_dotenv

from pages.login_page import LoginPage
from pages.meal_plan_page import MealPlanPage


load_dotenv()

BASE_URL = os.getenv("BASE_URL")

USERNAME = os.getenv("TANDOOR_USERNAME")

PASSWORD = os.getenv("TANDOOR_PASSWORD")


@allure.feature("Meal Plan")
@allure.story("View meal plan")
def test_view_meal_plan(
    driver,
    get_or_create_recipe
):

    meal_type = "Обед"

    servings = 4

    notes = "Автотест meal plan"

    login_page = LoginPage(driver)

    meal_plan_page = MealPlanPage(driver)

    with allure.step("Открыть страницу логина"):

        login_page.open(BASE_URL)

    with allure.step("Авторизоваться"):

        login_page.login(
            USERNAME,
            PASSWORD
        )

    with allure.step("Открыть страницу Meal Plan"):

        meal_plan_page.open_meal_plan_page(
            BASE_URL
        )

    with allure.step("Нажать на день календаря"):

        meal_plan_page.click_calendar_day()

    random_recipe = random.choice(
        get_or_create_recipe
    )

    recipe_name = random_recipe["name"]

    with allure.step(f"Выбрать рецепт: {recipe_name}"):

        meal_plan_page.select_recipe(
            recipe_name
        )

    with allure.step("Изменить диапазон дат"):

        for _ in range(random.randint(1, 3)):

            random.choice([
                meal_plan_page.increase_date_range,
                meal_plan_page.next_date_range
            ])()

    with allure.step(f"Выбрать тип питания: {meal_type}"):

        meal_plan_page.select_meal_type(
            meal_type
        )

    time.sleep(1)

    with allure.step(f"Установить servings: {servings}"):

        meal_plan_page.set_servings(
            servings
        )

    with allure.step("Выключить Add to shopping list"):

        meal_plan_page.set_add_to_shopping_list(
            False
        )

    with allure.step("Добавить notes"):

        meal_plan_page.enter_notes(
            notes
        )

    with allure.step("Создать Meal Plan"):

        meal_plan_page.create_meal_plan()

    with allure.step("Проверить успешное создание Meal Plan"):

        assert meal_plan_page.is_create_successful()

    with allure.step("Обновить страницу"):

        meal_plan_page.refresh_page()

    with allure.step("Открыть созданный Meal Plan"):

        meal_plan_page.open_created_meal_plan(
            recipe_name
        )

    with allure.step("Проверить notes"):

        assert notes in meal_plan_page.get_notes_value()

    with allure.step("Проверить servings"):

        assert float(
            meal_plan_page.get_servings_value().replace(",", ".")
        ) == float(servings)

    with allure.step("Открыть рецепт из Meal Plan"):

        meal_plan_page.open_recipe_from_meal_plan()

    with allure.step("Переключиться на новую вкладку"):

        driver.switch_to.window(
            driver.window_handles[1]
        )

    with allure.step("Проверить URL рецепта"):

        assert "/recipe/" in driver.current_url

    with allure.step("Закрыть вкладку рецепта"):

        driver.close()

    with allure.step("Вернуться на вкладку Meal Plan"):

        driver.switch_to.window(
            driver.window_handles[0]
        )

    with allure.step("Удалить Meal Plan"):

        meal_plan_page.delete_meal_plan()