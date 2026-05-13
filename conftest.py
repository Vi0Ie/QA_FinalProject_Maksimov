import json
import os

import pytest

from api.client import TandoorAPIClient

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def api_client():

    return TandoorAPIClient()


@pytest.fixture
def recipe_data():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(
        base_dir,
        "data",
        "recipe_links.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:

        data = json.load(file)

    return data


@pytest.fixture
def get_or_create_recipe(
    api_client,
    recipe_data
):

    recipes = api_client.get_recipes()

    if not recipes["results"]:

        for recipe_url in recipe_data["recipes"]:

            api_client.import_recipe(
                recipe_url
            )

        recipes = api_client.get_recipes()

    return recipes["results"]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            screenshots_dir = "screenshots"

            os.makedirs(screenshots_dir, exist_ok=True)

            screenshot_path = os.path.join(
                screenshots_dir,
                f"{item.name}.png"
            )

            driver.save_screenshot(screenshot_path)

            print(f"Screenshot saved: {screenshot_path}")


@pytest.fixture
def driver():

    chrome_options = Options()

    chrome_options.add_argument("--headless")

    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=chrome_options
    )

    yield driver

    driver.quit()