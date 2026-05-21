import allure
import pytest

from api.client import TandoorAPIClient


@pytest.mark.api
@allure.feature("API")
@allure.story("Get recipes without fixture")
def test_get_recipes():

    with allure.step("Создать API client"):

        api_client = TandoorAPIClient()

    with allure.step("Получить список рецептов"):

        response = api_client.get_recipes()

    with allure.step("Проверить что ответ не None"):

        assert response is not None