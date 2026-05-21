import os

import time

import pytest

import allure

from dotenv import load_dotenv

from pages.login_page import LoginPage
from components.header_component import HeaderComponent


load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("TANDOOR_USERNAME")
PASSWORD = os.getenv("TANDOOR_PASSWORD")


@pytest.mark.ui
@allure.feature("Authentication")
@allure.story("User login")
@allure.title("Successful user login")
@allure.description("""
Checks that user can successfully login
into Tandoor Recipes application.
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_user_logged_in(driver):

    login_page = LoginPage(driver)

    header = HeaderComponent(driver)

    with allure.step("Открыть страницу логина"):

        login_page.open(BASE_URL)

    with allure.step("Авторизоваться"):

        login_page.login(
            USERNAME,
            PASSWORD
        )

    time.sleep(2)

    with allure.step("Проверить что пользователь залогинен"):

        assert header.is_user_logged_in()
