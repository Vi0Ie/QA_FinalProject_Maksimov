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


@allure.feature("Shopping List")
@allure.story("Shopping list validation")
def test_shopping_list(
    driver,
    get_or_create_recipe,
    api_client
):

    meal_type = "Обед"

    servings = 2

    notes = f"Shopping list test {time.time()}"

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

    with allure.step("Включить Add to shopping list"):

        meal_plan_page.set_add_to_shopping_list(
            True
        )

    with allure.step("Проверить что shopping list включён"):

        print(
            meal_plan_page.is_add_to_shopping_list_enabled()
        )

    with allure.step("Добавить notes"):

        meal_plan_page.enter_notes(
            notes
        )

    meal_plan_created = False

    try:

        with allure.step("Создать Meal Plan"):

            meal_plan_page.create_meal_plan()

        with allure.step("Проверить успешное создание"):

            assert meal_plan_page.is_create_successful()

        meal_plan_created = True

        time.sleep(2)

        with allure.step("Открыть вкладку Shopping List"):

            meal_plan_page.open_shopping_list_tab()

        time.sleep(2)

        with allure.step("Проверить что shopping list не пустой"):

            assert meal_plan_page.is_shopping_list_not_empty()

    finally:

        if meal_plan_created:

            with allure.step("Удалить Meal Plan"):

                meal_plan_page.delete_meal_plan()

            with allure.step("Проверить удаление Meal Plan"):

                assert meal_plan_page.is_meal_plan_deleted(
                    recipe_name
                )