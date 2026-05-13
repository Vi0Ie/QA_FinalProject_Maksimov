import allure


@allure.feature("API")
@allure.story("Get recipes")
def test_get_recipes(api_client):

    with allure.step("Получить список рецептов"):

        response = api_client.get_recipes()

    with allure.step("Проверить что ответ не None"):

        assert response is not None

    with allure.step("Проверить что ответ является словарём"):

        assert isinstance(response, dict)

    with allure.step("Проверить наличие поля results"):

        assert "results" in response


@allure.feature("API")
@allure.story("Import recipe")
def test_import_recipe(api_client, recipe_data):

    recipe_url = recipe_data["recipes"][0]

    with allure.step(f"Импортировать рецепт: {recipe_url}"):

        response = api_client.import_recipe(
            recipe_url
        )

    with allure.step("Проверить что рецепт импортирован"):

        assert response is not None

    with allure.step("Проверить наличие name"):

        assert "name" in response

    with allure.step("Проверить наличие id"):

        assert "id" in response


@allure.feature("API")
@allure.story("Delete recipe")
def test_delete_recipe(api_client, recipe_data):

    recipe_url = recipe_data["recipes"][0]

    with allure.step(f"Импортировать рецепт: {recipe_url}"):

        imported_recipe = api_client.import_recipe(
            recipe_url
        )

    with allure.step("Проверить что рецепт импортирован"):

        assert imported_recipe is not None

    recipe_id = imported_recipe["id"]

    with allure.step(f"Удалить рецепт ID={recipe_id}"):

        delete_response = api_client.delete_recipe(
            recipe_id
        )

    with allure.step("Проверить успешное удаление"):

        assert delete_response == 204

    with allure.step("Получить список рецептов"):

        recipes = api_client.get_recipes()

    with allure.step("Проверить что рецепт удалён"):

        recipe_ids = [
            recipe["id"]
            for recipe in recipes["results"]
        ]

        assert recipe_id not in recipe_ids


@allure.feature("API")
@allure.story("API connection")
def test_api_connection(api_client):

    with allure.step("Проверить соединение с API"):

        response = api_client.get_recipes()

    with allure.step("Проверить что ответ не None"):

        assert response is not None

    with allure.step("Проверить наличие поля results"):

        assert "results" in response


@allure.feature("API")
@allure.story("API headers")
def test_api_client_headers(api_client):

    with allure.step("Проверить наличие headers"):

        assert api_client.headers is not None

    with allure.step("Проверить наличие Authorization header"):

        assert "Authorization" in api_client.headers
