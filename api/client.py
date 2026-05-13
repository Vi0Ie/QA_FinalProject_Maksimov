import os

import requests
from dotenv import load_dotenv


load_dotenv()


class TandoorAPIClient:

    def __init__(self):

        self.base_url = os.getenv("BASE_URL")
        self.token = os.getenv("TANDOOR_TOKEN")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method, endpoint, data=None):

        url = f"{self.base_url}{endpoint}"

        try:

            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )

            response.raise_for_status()

            return response

        except requests.exceptions.HTTPError as error:
            print(f"HTTP error: {error}")

        except requests.exceptions.ConnectionError as error:
            print(f"Connection error: {error}")

        except requests.exceptions.Timeout as error:
            print(f"Timeout error: {error}")

        except requests.exceptions.RequestException as error:
            print(f"Request error: {error}")

        return None

    def import_recipe(self, recipe_url):

        data = {
            "url": recipe_url
        }

        response = self._make_request(
            method="POST",
            endpoint="/api/recipe-from-source/",
            data=data
        )

        if response:
            imported_recipe = response.json()

            recipe_data = imported_recipe["recipe"]

            created_recipe = self.create_recipe(recipe_data)

            print("CREATED RECIPE:")
            print(created_recipe)

            return created_recipe

        return None

    def create_recipe(self, recipe_data):

        response = self._make_request(
            method="POST",
            endpoint="/api/recipe/",
            data=recipe_data
        )

        if response and response.status_code in [200, 201]:
            return response.json()

        return None

    def get_recipes(self):

        response = self._make_request(
            method="GET",
            endpoint="/api/recipe/"
        )

        return response.json()

    def delete_recipe(self, recipe_id):

        response = self._make_request(
            method="DELETE",
            endpoint=f"/api/recipe/{recipe_id}/"
        )

        return response.status_code

    def create_meal_plan(self, data):

        response = self._make_request(
            method="POST",
            endpoint="/api/meal-plan/",
            data=data
        )

        if response and response.status_code in [200, 201]:
            return response.json()

        return None

    def get_meal_plan(self, meal_plan_id):

        response = self._make_request(
            method="GET",
            endpoint=f"/api/meal-plan/{meal_plan_id}/"
        )

        if response and response.status_code == 200:
            return response.json()

        return None

    def delete_meal_plan(self, meal_plan_id):

        response = self._make_request(
            method="DELETE",
            endpoint=f"/api/meal-plan/{meal_plan_id}/"
        )

        if response:
            return response.status_code

        return None

    def get_shopping_list(self):

        response = self._make_request(
            method="GET",
            endpoint="/api/shopping-list/"
        )

        if response and response.status_code == 200:
            return response.json()

        return None

    def get_meal_plans(self):

        response = self._make_request(
            method="GET",
            endpoint="/api/meal-plan/"
        )

        if response and response.status_code == 200:
            return response.json()

        return None

    def test_connection(self):

        response = self.get_recipes()

        if response:
            print("Connection successful")
            print(response)

        else:
            print("Connection failed")

if __name__ == "__main__":

    client = TandoorAPIClient()

    client.test_connection()