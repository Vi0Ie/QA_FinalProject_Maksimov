import os

import allure

from dotenv import load_dotenv

from pages.login_page import LoginPage
from components.header_component import HeaderComponent


load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("TANDOOR_USERNAME")
PASSWORD = os.getenv("TANDOOR_PASSWORD")


@allure.feature("Authentication")
@allure.story("User login")
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

    with allure.step("Проверить что пользователь залогинен"):

        assert header.is_user_logged_in()