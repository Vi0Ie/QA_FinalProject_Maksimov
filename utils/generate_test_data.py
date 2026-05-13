import json
import os

from datetime import datetime, timedelta

from api.client import TandoorAPIClient


def generate_meal_plan_data():

    api_client = TandoorAPIClient()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(
        base_dir,
        "data",
        "recipe_links.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:

        recipe_data = json.load(file)

    recipe_ids = []

    for recipe_url in recipe_data["recipes"]:

        print(f"Importing recipe: {recipe_url}")

        response = api_client.import_recipe(recipe_url)

        if response and response.get("recipe_id"):

            recipe_ids.append(response["recipe_id"])

            print("Recipe imported successfully")

    start_date = datetime.now().date()

    end_date = start_date + timedelta(days=7)

    meal_plan_data = []

    for recipe_id in recipe_ids:

        meal_plan = {
            "recipe": recipe_id,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "meal_type": "breakfast",
            "servings": 2
        }

        meal_plan_data.append(meal_plan)

    return meal_plan_data


if __name__ == "__main__":

    data = generate_meal_plan_data()

    print(data)