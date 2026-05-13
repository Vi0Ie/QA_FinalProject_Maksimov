import os
import json
import allure

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

        allure.attach(
            f"{method} {url}",
            name="Request",
            attachment_type=allure.attachment_type.TEXT
        )

        if data:
            allure.attach(
                json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False
                ),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON
            )

        try:

            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )

            allure.attach(
                str(response.status_code),
                name="Status Code",
                attachment_type=allure.attachment_type.TEXT
            )

            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

            response.raise_for_status()

            return response

        except requests.exceptions.HTTPError as error:

            allure.attach(
                str(error),
                name="HTTP Error",
                attachment_type=allure.attachment_type.TEXT
            )

        except requests.exceptions.ConnectionError as error:

            allure.attach(
                str(error),
                name="Connection Error",
                attachment_type=allure.attachment_type.TEXT
            )

        except requests.exceptions.Timeout as error:

            allure.attach(
                str(error),
                name="Timeout Error",
                attachment_type=allure.attachment_type.TEXT
            )

        except requests.exceptions.RequestException as error:

            allure.attach(
                str(error),
                name="Request Error",
                attachment_type=allure.attachment_type.TEXT
            )

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

        if response:
            return response.json()

        return None

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