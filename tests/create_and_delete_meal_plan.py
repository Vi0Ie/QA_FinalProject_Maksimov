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
@allure.story("Create and delete meal plan")
def test_create_meal_plan(
    driver,
    get_or_create_recipe,
    api_client
):

    meal_type = "Обед"

    servings = 4

    notes = f"Автотест meal plan {time.time()}"

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

    with allure.step("Отключить shopping list"):

        meal_plan_page.set_add_to_shopping_list(
            False
        )

    with allure.step("Добавить notes"):

        meal_plan_page.enter_notes(
            notes
        )

    meal_plan_created = False

    meal_plan_id = None

    try:

        with allure.step("Создать Meal Plan"):

            meal_plan_page.create_meal_plan()

        with allure.step("Проверить успешное создание"):

            assert meal_plan_page.is_create_successful()

        meal_plan_created = True

        with allure.step("Получить meal plans через API"):

            meal_plans = api_client.get_meal_plans()

        with allure.step("Найти созданный meal plan"):

            for plan in meal_plans["results"]:

                if (
                        plan["recipe_name"] == recipe_name
                        and plan["note"] == notes
                        and float(plan["servings"]) == float(servings)
                ):
                    meal_plan_id = plan["id"]

                    break

            assert meal_plan_id is not None

    finally:

        if meal_plan_created:

            with allure.step("Удалить Meal Plan"):

                meal_plan_page.delete_meal_plan()

            with allure.step("Проверить удаление Meal Plan"):

                assert meal_plan_page.is_meal_plan_deleted(
                    recipe_name
                )

            time.sleep(1)

            deleted_plan = api_client.get_meal_plan(
                meal_plan_id
            )

            assert deleted_plan is None